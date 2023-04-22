from typing import Union

from requests import post

from conf.push import push_setting
from push.base import PushBase


class Mirai(PushBase):
    def _send_update(self,
                     task: str,
                     title: str,
                     url: str,
                     subscriber: dict) -> bool:
        def _mirai_http_auth() -> Union[str, bool]:
            """
            Mirai HTTP接口身份验证。

            :return: 如果完成身份验证，返回会话密钥，否则返回False
            """
            try:
                auth_string = {
                    'verifyKey': push_setting['mirai']['verify_key']
                }
                result = post(f'http://{push_setting["mirai"]["host"]}/verify', json=auth_string).json()
                if int(result['code']) == 0:
                    bind_string = {
                        'sessionKey': result['session'],
                        'qq': push_setting['mirai']['sender']
                    }
                    result = post(f'http://{push_setting["mirai"]["host"]}/bind', json=bind_string).json()
                    if int(result['code']) == 0:
                        return bind_string['sessionKey']
                    else:
                        _mirai_http_release(bind_string['sessionKey'])
                        return False
                else:
                    return False
            except Exception:
                return False

        def _mirai_http_release(
                session_key: str) -> bool:
            """
            释放本次Mirai HTTP会话。

            :param session_key: 待释放的会话密钥
            :return: True：成功 | False：失败
            """
            release_string = {
                'sessionKey': session_key,
                'qq': push_setting['mirai']['sender']
            }
            try:
                if int(post(f'http://{push_setting["mirai"]["host"]}/release', json=release_string).json()[
                           'code']) == 0:
                    return True
                else:
                    return False
            except Exception:
                return False

        auth_result = _mirai_http_auth()
        push_result = False
        if auth_result:
            headers = {
                'Content-Type': 'application/json'
            }
            message_string = {
                'sessionKey': auth_result,
                'target': subscriber['id'],
                'messageChain': [
                    {'type': 'Plain', 'text': f'{task}发现更新：\n'},
                    {'type': 'Plain', 'text': f'{title}\n'},
                    {'type': 'Plain', 'text': url}
                ]
            }
            request_format = 'sendGroupMessage' if subscriber['is_group'] else 'sendFriendMessage'
            try:
                if int(post(f'http://{push_setting["mirai"]["host"]}/{request_format}', json=message_string,
                            headers=headers).json()['code']) == 0:
                    push_result = True
            except Exception:
                pass
        _mirai_http_release(auth_result)
        return push_result
