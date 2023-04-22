from abc import ABC, abstractmethod
from inspect import getfile
from os.path import basename


class PushBase(ABC):
    def __init__(self,
                 task: str,
                 title: str,
                 url: str,
                 subscribers: list):
        """
        更新推送的抽象类，继承此类并实现_send_update方法即可注册为一个有效的推送方法。
        注意：实现方法后请前往conf/subscribers.py文件中添加用户参数（必须包含enable参数），
        前往conf/push.py添加该种推送方法所需（如有）的参数。

        :param task: 任务名
        :param title: 消息标题
        :param url: 消息链接
        :param subscribers: 用户列表
        """
        push_name = basename(getfile(self.__class__))[: basename(getfile(self.__class__)).rfind('.')]
        enabled_subscribers = [
            subscriber[push_name]
            for subscriber in subscribers
            if (subscriber[push_name]['enable']) and ((subscriber['range'] is True) or (task in subscriber['range']))
        ]
        self._failed_push = {
            'task': task,
            'title': title,
            'url': url,
            'subscribers': []
        }
        for subscriber in enabled_subscribers:
            if not self._send_update(task, title, url, subscriber):
                self._failed_push['subscribers'].append(subscriber)

    def get_failed_push(self):
        """
        当推送失败时，使用此方法获取未能成功送达的用户列表。

        :return: 推送未能送达的用户列表及对应的消息内容
        """
        return self._failed_push

    @abstractmethod
    def _send_update(self,
                     task: str,
                     title: str,
                     url: str,
                     subscriber: dict) -> bool:
        """
        推送的消息发送方式，推送类的最关键方法，必须在子类中实现才能使用。
        请自行捕获异常，如果推送发送失败返回False，成功返回True。

        :param task: 任务名
        :param title: 消息标题
        :param url: 消息链接
        :param subscriber: 用户
        :return: True：成功 | False：失败
        """
        pass
