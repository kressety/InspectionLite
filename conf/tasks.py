from urllib.parse import urljoin

from core.parse import task_url_parse
from re import findall

task_list = [
    'CSP通知',
    '工大教务处', 
#     将你的任务添加在这里。
#     下面两个函数是任务的主要流程，请仔细阅读两个示例，并按照相同格式填写。
]


def get_task_url(task_name: str) -> str:
    """
    获取指定任务的URL。

    :param task_name: 任务名
    :return: URL
    """
    if task_name == task_list[0]:
        jump_request = task_url_parse('https://www.cspro.org/cms/show.action?code=jumpchanneltemplate')
        return urljoin('https://www.cspro.org', findall('\".*\"', jump_request.script.text)[1].strip('\"'))
    elif task_name == task_list[1]:
        return 'http://jwc.njtech.edu.cn/'


def get_task_css(task_name: str) -> str:
    """
    获取指定任务的CSS选择器。

    :param task_name: 任务名
    :return: CSS选择器
    """
    if task_name == task_list[0]:
        return 'body > div.l_mainouter > div > div:nth-child(1) > div.l_newsmsg.clearfix > div.l_overflowhidden > ' \
               'span > a '
    elif task_name == task_list[1]:
        return '#notice > div.ct > ul > li > p > a'
