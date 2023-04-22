# InspectionLite
InspectionLite 是一个用于检测指定 Web 页面更新的 Python 项目。它能够根据用户定义的任务列表，自动地检测指定页面的更新情况，并将更新信息推送给指定的用户。

[*English Version*](https://github.com/kressety/InspectionLite/blob/main/README-en.md)

# 特点
- **支持多种推送方式**：该程序支持多种推送方式，如 ~~企业微信、钉钉、~~ (待实现) 基于Mirai HTTP的QQ机器人和SMTP邮件等，能够满足不同用户的推送需求。
- **可自定义任务**：InspectionLite支持从配置文件中读取任务列表，用户可以根据自己的需求添加新的检测任务。
- **易于扩展**：程序采用模块化设计，用户可以方便地编写新的推送方法并注册到系统中。
- **定制化程度高**：用户可以根据自己的需求进行相应的配置，如修改数据库连接信息、任务列表、推送方式等。
- **可靠性强**：程序运行稳定可靠，能够在出现异常情况时及时发送邮件告知管理员。

# 安装
1. 克隆仓库到本地
2. 进入项目目录
3. 安装依赖：`pip install -r requirements.txt`
4. 配置程序参数：编辑`/conf`目录下的配置文件，根据需要修改参数值。
5. 运行程序：`python main.py`

# 使用示例
<details>
  <summary>1. 修改 conf/push.py 文件</summary>

```python
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
```

</details>

<details>
  <summary>2. 修改 conf/sql.py 文件</summary>

```python
# 项目使用MySQL数据库，因此在这里填写数据库的登录参数。
# 注意：数据库用户必须拥有该数据库的读/写权限。
sql_setting = {
    'host': '数据库地址',
    'user': '数据库用户名',
    'password': '数据库密码',
    'db': '要使用的数据库'
}
```

</details>

<details>
  <summary>3. 修改 conf/subscribers.py 文件</summary>

```python
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
```

</details>

<details>
  <summary>4. 修改 conf/tasks.py 文件</summary>

```python
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
```

</details>

<details>
  <summary>(可选) 5. 在 push 目录下添加自己的推送方式</summary>

```python
# 要实现自己的推送方式，必须继承 push.base.PushBase 类。
# 然后，你只需要实现 _send_update 方法即可。
from push.base import PushBase


class MyPush(PushBase):
    def _send_update(self,
                     task: str,
                     title: str,
                     url: str,
                     subscriber: dict) -> bool:
        # 在这里实现你的推送方法。
        # 假设在这里你使用了mypush.py作为你的文件名，那么：
        # 1. 在conf/push.py的push_setting['mypush']中放置你需要使用的全局参数（如有必要）；
        # 2. 在conf/subscribers.py的subscribers[index]['mypush']中放置每个用户的个人参数。
        pass
```

</details>

# 技术细节
### InspectionLite 项目主要包含以下几个模块：

- `main.py`：程序入口，负责创建数据库连接和任务单元。
- `/conf`目录：存放程序的配置文件，如MySQL连接信息、推送方式和任务列表等。
- `/core`目录：存放程序的核心代码，如任务检测、数据存储和推送功能的实现。
- `/push`目录：存放不同的推送方式的具体实现。

### InspectionLite 的工作流程如下：

- 根据任务列表获取需要检测的 Web 页面 URL 和 CSS 选择器。
- 检测 Web 页面更新情况，若发生更新则将更新记录保存到 MySQL 数据库中。
- 使用多种推送方式向指定用户发送更新通知。
- 如果出现推送失败的情况，则进行重试，并在重试失败时向管理员发送邮件告知具体情况。
- 整个程序运行在主程序上，可自动执行任务检测和推送操作。