# InspectionLite
InspectionLite is a Python project used to detect updates on specified web pages. It can automatically detect updates on the specified page based on the user-defined task list and push update notifications to specified users.

# Features
- **Supports multiple notification methods**: This program supports multiple notification methods, such as QQ bot based on Mirai HTTP, SMTP emails, etc., to meet the different needs of users.
- **Customizable tasks**: InspectionLite supports reading the task list from the configuration file. Users can add new detection tasks according to their needs.
- **Easy to extend**: The program adopts a modular design, and users can easily write new notification methods and register them in the system.
- **High degree of customization**: Users can configure parameters according to their own needs, such as modifying database connection information, task lists, notification methods, etc.
- **High reliability**: The program runs stably and reliably, and can promptly send emails to administrators in case of abnormal situations.

# Installation
1. Clone the repository to your local machine.
2. Enter the project directory.
3. Install dependencies: `pip install -r requirements.txt`
4. Configure program parameters: edit the configuration file in the `/conf` directory and modify parameter values as needed.
5. Run the program: `python main.py`.

# Usage Examples
<details>
  <summary>1. Modify the conf/push.py file</summary>

```python
push_setting = {
    # The administrator's email address. If there are any notification errors during runtime, they will be sent to this email address.
    'admin': {
       'email': 'admin@example.com'
    },
    # Fill in the parameters for the Mirai notification protocol here.
    # If you don't need Mirai notification, leave it blank.
    # Note: This project defaults to using Mirai HTTP protocol for notification.
    'mirai': {
        'host': 'mirai.host.com:port',
        'verify_key': 'Mirai HTTP verify key',
        # Fill in the sender's QQ number here. The sender must have logged in to Mirai Console.
        'sender': 10000
    },
    # Fill in the parameters for the SMTP (email) notification protocol here.
    # This is required because messages will be sent via email in case of notification errors.
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
  <summary>2. Modify the conf/sql.py file</summary>

```python
# The project uses a MySQL database, so fill in the login parameters for the database here.
# Note: The database user must have read/write permission for the database.
sql_setting = {
    'host': 'database address',
    'user': 'database username',
    'password': 'database password',
    'db': 'database to use'
}
```

</details>

<details>
  <summary>3. Modify the conf/subscribers.py file</summary>

```python
subscribers = [
    # User 1
    {
        # If subscribing to all notifications, set range to True;
        # If subscribing to some notifications, write them as a list here;
        # If subscribing to no notifications, set range to False (or delete this user).
        'range': True,
        'mirai': {
            # Enable Mirai notification by setting enable to True.
            # If not using Mirai notification, ignore id and is_group.
            'enable': True,
            'id': 10001,
            'is_group': False,
        },
        'smtp': {
            # Enable SMTP (email) notification by setting enable to True.
            # If not using SMTP notification, ignore email.
            'enable': True,
            'email': 'user@example.com'
        }
    },
    # User 2
    {
        'range': ['CSP notifications'],
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
  <summary>4. Modify the conf/tasks.py file</summary>

```python
task_list = [
    'CSP notifications',
    'NJ Tech Academic Affairs Office', 
#     Add your tasks here.
#     The following two functions are the main process of the task. Please read the examples carefully and fill in the same format.
]


def get_task_url(task_name: str) -> str:
    """
    Get the URL of the specified task.

    :param task_name: Task name
    :return: URL
    """
    if task_name == task_list[0]:
        jump_request = task_url_parse('https://www.cspro.org/cms/show.action?code=jumpchanneltemplate')
        return urljoin('https://www.cspro.org', findall('\".*\"', jump_request.script.text)[1].strip('\"'))
    elif task_name == task_list[1]:
        return 'http://jwc.njtech.edu.cn/'


def get_task_css(task_name: str) -> str:
    """
    Get the CSS selector of the specified task.

    :param task_name: Task name
    :return: CSS selector
    """
    if task_name == task_list[0]:
        return 'body > div.l_mainouter > div > div:nth-child(1) > div.l_newsmsg.clearfix > div.l_overflowhidden > ' \
               'span > a '
    elif task_name == task_list[1]:
        return '#notice > div.ct > ul > li > p > a'
```

</details>

<details>
  <summary>(Optional) 5. Add your own notification method under the push directory</summary>

```python
# To implement your own notification method, you must inherit the push.base.PushBase class.
# Then, you only need to implement the _send_update method.
from push.base import PushBase


class MyPush(PushBase):
    def _send_update(self,
                     task: str,
                     title: str,
                     url: str,
                     subscriber: dict) -> bool:
        # Implement your notification method here.
        # Suppose you use mypush.py as your file name here:
        # 1. Put the global parameters you need to use in push_setting['mypush'] in conf/push.py (if necessary);
        # 2. Put individual parameters for each user in subscribers[index]['mypush'] in conf/subscribers.py.
        pass
```

</details>

# Technical Details
### The InspectionLite project mainly consists of the following modules: 

- `main.py`: Program entry point, responsible for creating database connections and task units.
- `/conf` directory: Stores the program's configuration files, such as MySQL connection information, notification methods, and task lists.
- `/core` directory: Stores the core code of the program, such as task detection, data storage, and notification function implementations.
- `/push` directory: Stores specific implementations of different notification methods.

### The workflow of InspectionLite is as follows: 

- Obtain the Web page URL and CSS selector to be detected based on the task list.
- Detect the update status of the Web page, and if an update occurs, save the update record to the MySQL database.
- Use multiple notification methods to send update notifications to specified users.
- If a notification failure occurs, retry and email the administrator with details if the retry fails.
- The entire program runs on the main program and can automatically perform task detection and notification operations.