from pymysql import connect, Error


def set_task_sql_connect(
        host: str,
        user: str,
        password: str,
        db: str) -> connect:
    """
    建立数据库连接。

    :param host: 数据库地址
    :param user: 数据库用户名
    :param password: 数据库密码
    :param db: 数据库名
    :return: 数据库连接
    """
    return connect(host=host, user=user, password=password, db=db)


def task_table_initialization(
        database: connect,
        table_name: str) -> bool:
    """
    初始化数据表，如果不存在则新建

    :param database: 数据库连接
    :param table_name: 数据表名
    :return: True：初始化成功 | False：初始化失败
    """
    try:
        with database.cursor() as database_cursor:
            database_cursor.execute(f"""
            create table if not exists {table_name}(
                title text not null,
                url   text not null
            )""")
            database.commit()
            database_cursor.close()
        return True
    except Error:
        return False


def task_table_check(
        database: connect,
        table_name: str,
        title: str,
        url: str) -> bool:
    """
    检查表中是否已存在指定行。

    :param database: 数据库连接
    :param table_name: 数据表名
    :param title: 标题
    :param url: 链接
    :return: True：已存在或出现错误 | False：不存在
    """
    try:
        with database.cursor() as database_cursor:
            result = database_cursor.execute(f"select * from {table_name} where title='{title}' and url='{url}'")
            database_cursor.close()
        if result > 0:
            return True
        else:
            return False
    except Error:
        return True


def task_table_insert(
        database: connect,
        table_name: str,
        title: str,
        url: str):
    """
    向数据表中插入指定行。

    :param database: 数据库连接
    :param table_name: 数据表名
    :param title: 标题
    :param url: 链接
    """
    try:
        with database.cursor() as database_cursor:
            database_cursor.execute(f"insert into {table_name} (title, url) VALUES ('{title}', '{url}')")
            database.commit()
            database_cursor.close()
    except Error:
        pass
