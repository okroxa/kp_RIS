
import pymysql
import pymysql.err as OperationalError

class DBConnection:
    def __init__(self, config: dict): # конструктор инициализации объекта, принимает config (словарь)
        self.config = config
        self.cursor = None
        self.connection = None

    def __enter__(self): # установка соединения с базой данных
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except OperationalError:
            return None

    def __exit__(self, exc_type, exc_val, exc_trace): # завершение соединения с базой данных (уборка)
        if self.connection is not None and self.cursor is not None:
            self.connection.commit()
            self.connection.close()
            self.cursor.close()
        if exc_val is not None:
            print(exc_type)
            print(exc_val.args)
        return True


def work_with_db(dbconfig: dict, sql: str):
    result = []
    with DBConnection(dbconfig) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))
    return result


def db_update(dbconfig: dict, _sql):
    with DBConnection(dbconfig) as cursor:
        cur = cursor.execute(_sql)
    return cur