subscribers = [
    # 这里是 1 号用户
    {
        # 订阅的推送，如果全部订阅则将 range 设置为 True；
        # 如果部分订阅，则将订阅的内容以 list 的形式写在这里；
        # 如果不订阅任何内容，则将 range 置为 False （或者你可以直接删除这个用户）。
        'range': True,
        'mirai': {
            # 启用则将 enable 置为 True。
            'enable': True,
            # 如果不启用 Mirai 推送，则 id 和 is_group 的值都会被忽略。
            'id': 10001,
            # 如果推送目标是一个QQ群，则将 is_group 置为 True；
            # 如果推送给单个用户，则此项为 False。
            'is_group': False,
        },
        'smtp': {
            # 同上，启用则置为 True。
            'enable': True,
            # 如果启用，则填写 email，否则此项会被忽略，不需要填写。
            'email': 'user@example.com'
        }
    },
    # 这里是 2 号用户
    {
        'range': ['CSP通知'],
        'mirai': {
            'enable': True,
            'id': 20001,
            'is_group': True,
        },
        'smtp': {
            'enable': False
        }
    }
]