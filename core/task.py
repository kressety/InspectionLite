from email.mime.text import MIMEText
from email.utils import make_msgid, formataddr, parseaddr
from importlib import import_module
from json import dumps
from os import listdir
from smtplib import SMTPException, SMTP_SSL
from time import sleep
from urllib.parse import urljoin, urlparse

from pymysql import connect
from pypinyin import slug

from conf.push import push_setting
from conf.tasks import get_task_url, get_task_css
from core.parse import task_url_parse
from core.sql import task_table_initialization, task_table_check, task_table_insert


def _push_register() -> list:
    """
    注册推送方法。

    :return: 推送方法列表
    """
    push_methods = [
        push_method_file[: push_method_file.rfind('.')]
        for push_method_file in listdir('push')
        if (push_method_file.endswith('.py')) and (push_method_file != 'base.py')
    ]
    for push_method_file_index in range(len(push_methods)):
        push_method_module = import_module(f'push.{push_methods[push_method_file_index]}')
        push_methods[push_method_file_index] = eval(f'push_method_module.{push_method_module.__dir__()[-1]}')
    return push_methods


def _failure_process(failure_list: list):
    try:
        mail_server = SMTP_SSL(push_setting['smtp']['host'])
        mail_server.connect(
            push_setting['smtp']['host'],
            push_setting['smtp']['port']
        )
        mail_server.login(
            push_setting['smtp']['username'],
            push_setting['smtp']['password']
        )

        message = MIMEText(
            dumps(
                failure_list,
                indent=4,
                ensure_ascii=False
            ),
            'plain',
            'utf-8'
        )
        message['From'] = formataddr(
            parseaddr(f"Inspection自动提醒 <{push_setting['smtp']['username']}>"),
            'utf-8'
        )
        message['To'] = formataddr(
            parseaddr(push_setting['admin']['email']),
            'utf-8'
        )
        message['Subject'] = 'Inspection自动提醒：推送失败'
        message['Message-ID'] = make_msgid()

        mail_server.sendmail(
            push_setting['smtp']['username'],
            push_setting['admin']['email'],
            message.as_string()
        )
        sleep(5)
        mail_server.close()
        return True
    except SMTPException:
        return False


class Task:
    def __init__(self,
                 task: str,
                 subscribers: list,
                 sql_connect: connect):
        """
        Inspection任务单元。

        :param task: 任务名
        :param subscribers: 用户列表
        :param sql_connect: 数据库连接
        """
        self.task = task
        self.url = get_task_url(task)
        self.css_selector = get_task_css(task)
        self.subscribers = subscribers
        self.sql_connect = sql_connect
        self.push_methods = _push_register()

        self.table_name = slug(task, separator='')
        if task_table_initialization(
                self.sql_connect,
                self.table_name):
            self._update()

    def _update(self):
        retry_list = []
        failure_list = []

        task_request = task_url_parse(self.url)
        if task_request:
            for item in task_request.select(self.css_selector):
                write_title = item.text.strip()
                write_url = urljoin(
                    f'{urlparse(self.url).scheme}://{urlparse(self.url).hostname}',
                    item.attrs['href']
                )

                if not task_table_check(
                        self.sql_connect,
                        self.table_name,
                        write_title,
                        write_url):
                    for push_method in self.push_methods:
                        push_session = push_method(
                            self.task,
                            write_title,
                            write_url,
                            self.subscribers
                        )
                        failed_push = push_session.get_failed_push()
                        if failed_push['subscribers']:
                            failed_push['class'] = push_method
                            retry_list.append(failed_push)

                task_table_insert(
                    self.sql_connect,
                    self.table_name,
                    write_title,
                    write_url
                )

        if retry_list:
            for retry_push in retry_list:
                retry_session = retry_push['class'](
                    retry_push['task'],
                    retry_push['title'],
                    retry_push['url'],
                    retry_push['subscribers']
                )
                failed_push = retry_session.get_failed_push()
                if failed_push['subscribers']:
                    failed_push['class'] = retry_push['class']
                    failure_list.append(failed_push)

        if failure_list:
            _failure_process(failure_list)
