from email.mime.text import MIMEText
from email.utils import make_msgid, parseaddr, formataddr
from smtplib import SMTPException, SMTP_SSL
from time import sleep

from conf.push import push_setting
from push.base import PushBase


class SMTP(PushBase):
    def _send_update(self,
                     task: str,
                     title: str,
                     url: str,
                     subscriber: dict) -> bool:
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
                title + '\n' + url,
                'plain',
                'utf-8'
            )
            message['From'] = formataddr(
                parseaddr(f"Inspection自动提醒 <{push_setting['smtp']['username']}>"),
                'utf-8'
            )
            message['To'] = formataddr(
                parseaddr(subscriber['email']),
                'utf-8'
            )
            message['Subject'] = f'Inspection自动提醒：{task}'
            message['Message-ID'] = make_msgid()

            mail_server.sendmail(
                push_setting['smtp']['username'],
                subscriber['email'],
                message.as_string()
            )
            sleep(5)
            mail_server.close()
            return True
        except SMTPException:
            return False
