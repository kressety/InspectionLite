from conf.sql import sql_setting
from conf.subscribers import subscribers
from conf.tasks import task_list
from core.sql import set_task_sql_connect
from core.task import Task


def main():
    sql_connect = set_task_sql_connect(
        sql_setting['host'],
        sql_setting['user'],
        sql_setting['password'],
        sql_setting['db']
    )

    for task in task_list:
        Task(task, subscribers, sql_connect)

    sql_connect.close()


if __name__ == '__main__':
    main()
