#coding:utf8
import pymysql

class select():
    global Mysql_conn_config
    Mysql_conn_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'mysql_pass',
        'db': 'auth_user',
        'charset': 'utf8mb4',
    }
    def __init__(self):
        pass
    def check_part(username,part,insert):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        sql = "select %s from user where name='%s'"%(part,username)
        curr.execute(sql)
        res = curr.fetchall()
        if not res:
            yield '2'
            connection.close()
        elif res[0][0] == insert:
            yield '0'
            connection.close()
        else:
            yield '1'
            connection.close()
    def check_all_database(self):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        sql = "show databases;"
        curr.execute(sql)
        res = curr.fetchall()
        yield res
        connection.close()
if __name__ == '__main__':
    print(list(select.check_all_database(None)))