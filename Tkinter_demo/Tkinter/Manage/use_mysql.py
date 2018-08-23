#coding:utf-8
import pymysql
Mysql_conn_config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'mysql_pass',
          'db':'auth',
          'charset':'utf8mb4',
          }
class user_operating:
    def check_username(name):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        sql = "select name from userdb where name='%s'"%name
        try:
            curr.execute(sql)
            res = curr.fetchall()
            if not res:
                return('无此用户')
                connection.close()
            elif res[0][0] == name:
                return('成功')
                connection.close()
            else:
                return('失败')
                connection.close()
        except:
            return('无法连接数据库')
            connection.close()
    def check_adminuser(name):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        check_admin = "select info from userdb where name='%s'"%name
        try:
            curr.execute(check_admin)
            res = curr.fetchall()
            if not res:
                return('失败')
                connection.close()
            elif res[0][0] == 'admin_user':
                return('成功')
                connection.close()
            else:
                return('错误')
                connection.close()
        except:
            return('失败')
            connection.close()
    def check_userpass(name,password):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        sql = "select pass from userdb where name='%s'"%name
        try:
            curr.execute(sql)
            res = curr.fetchall()
            if not res:
                return('无此用户')
                connection.close()
            elif res[0][0] == password:
                return('成功')
                connection.close()
            else:
                return('失败')
                connection.close()
        except:
            return('无法连接数据库')
            connection.close()
    def create_user(name,password,info):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        check_sql = "select name from userdb where name='%s'"%name
        insert_sql = "insert into userdb(name,pass,info) value('%s','%s','%s')"%(name,password,info)
        try:
            curr.execute(check_sql)
            res = curr.fetchall()
            if not res:
                try:
                    curr.execute(insert_sql)
                    connection.commit()
                    return('成功')
                    connection.close()
                except:
                    return('失败')
                    connection.close()
            elif res[0][0] == name:
                return('用户已存在')
                connection.close()
            else:
                try:
                    curr.execute(insert_sql)
                    connection.commit()
                    return('成功')
                    connection.close()
                except:
                    return('失败')
                    connection.close()
        except:
            return('无法连接数据库')
            connection.close()
    def update_username(name,password,new_name):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        update_name = "update userdb set name='%s' where name='%s'"%(new_name,name)
        check_pass = "select pass from userdb where name='%s'"%name
        try:
            curr.execute(check_pass)
            res = curr.fetchall()
            if not res:
                return('无此用户')
                connection.close()
            elif res[0][0] == password:
                try:
                    curr.execute(update_name)
                    connection.commit()
                    return('成功')
                    connection.close()
                except:
                    return('错误')
                    connection.close()
            else:
                return('密码错误')
                connection.close()
        except:
            return('无法连接数据库')
            connection.close()
    def update_userpass(name,password,new_password):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        check_pass = "select pass from userdb where name='%s'"%name
        update_pass= "update userdb set pass='%s' where name='%s'"%(new_password,name)
        try:
            curr.execute(check_pass)
            res = curr.fetchall()
            if not res:
                return('无此用户')
                connection.close()
            elif res[0][0] == password:
                try:
                    curr.execute(update_pass)
                    connection.commit()
                    return('成功')
                    connection.close()
                except:
                    return('错误')
                    connection.close()
            else:
                return('密码错误')
                connection.close()
        except:
            return('无法连接数据库')
            connection.close()
    def delete_user(name,password,user):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        check_is_admin = "select pass from userdb where name='%s'"%name
        name_delete_user = "delete from userdb where name='%s'"%user
        id_delete_user = "delete from userdb where id='%s'"%user
        try:
            curr.execute(check_is_admin)
            res = curr.fetchall()
            if not res:
                return('无此用户')
                connection.close()
            elif res[0][0] == password:
                    if isinstance(user,str):
                        try:
                            curr.execute(name_delete_user)
                            connection.commit()
                            return('成功')
                            connection.close()
                        except:
                            return('失败1')
                            connection.close()
                    elif isinstance(user,int):
                        try:
                            curr.execute(id_delete_user)
                            connection.commit()
                            return('成功')
                            connection.close()
                        except:
                            return('失败2')
                            connection.close()
                    else:
                        return('失败3')
                        connection.close()
            else:
                return('失败5')
                connection.close()
        except:
            return('失败0')
            connection.close()
    def select_alluser(name,password):
        connection = pymysql.connect(**Mysql_conn_config)
        curr = connection.cursor()
        is_admin = "select pass from userdb where name='%s'"%name
        alluser = "select name,pass,mac from userdb"
        try:
            curr.execute(is_admin)
            res = curr.fetchall()
            if not res:
                return('失败')
                connection.close()
            elif res[0][0] == password:
                try:
                    curr.execute(alluser)
                    res = curr.fetchall()
                    return(res)
                    connection.close()
                except:
                    return('失败')
                    connection.close()
            else:
                return('失败')
                connection.close()
        except:
            return('失败')
            connection.close()