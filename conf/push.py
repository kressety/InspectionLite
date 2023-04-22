push_setting = {
    # 管理员邮箱，如果运行中出现推送错误则会发送到这个邮箱。
    'admin': {
       'email': 'admin@example.com'
    },
    # Mirai推送协议参数在这里填写，
    # 如果不需要Mirai推送则不需要填写。
    # 注意：本项目默认通过Mirai HTTP协议推送。
    'mirai': {
        'host': 'mirai.host.com:port',
        'verify_key': 'Mirai HTTP verify key',
        # 这里填写消息发送者的QQ号，必须已经在Mirai Console上登录
        'sender': 10000
    },
    # SMTP（电子邮箱）推送协议参数在这里填写。
    # 这里必须填写，因为出现推送错误会通过邮箱发送消息。
    'smtp': {
        'host': 'smtp.example.com',
        'port': 465,
        'username': 'inspectionlite@example.com',
        'password': 'example password'
    }
}