from typing import Union

from bs4 import BeautifulSoup
from requests import get, RequestException


def task_url_parse(url: str) -> Union[BeautifulSoup, bool]:
    """
    解析任务URL，并返回BeautifulSoup对象。

    :param url: 任务URL
    :return: 如果完成解析，返回BS对象，否则返回False
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77 '
    }
    try:
        request = get(url, headers=header)
        request.encoding = 'UTF-8'
        if request.status_code == 200:
            html_data = BeautifulSoup(request.text, features='html.parser')
            return html_data
        else:
            return False
    except RequestException:
        return False
