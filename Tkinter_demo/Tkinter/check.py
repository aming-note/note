#coding:utf-8
from tkinter import *
from tkinter import ttk
import pymysql
import time
def center_window(tl, width, height):
    screenwidth = tl.winfo_screenwidth()
    screenheight = tl.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    tl.geometry(size)
Mysql_conn_config = {
          'host':'118.24.23.29',
          'port':3306,
          'user':'root',
          'password':'123456',
          'db':'auth',
          'charset':'utf8mb4',
          }
def check_userpass(name, password):
    connection = pymysql.connect(**Mysql_conn_config)
    curr = connection.cursor()
    sql = "select pass from userdb where name='%s'" % name
    try:
        curr.execute(sql)
        res = curr.fetchall()
        if not res:
            return ('无此用户')
            connection.close()
        elif res[0][0] == password:
            return ('成功')
            connection.close()
        else:
            return ('失败')
            connection.close()
    except:
        return ('无法连接数据库')
        connection.close()


root = Tk()
root.title('资源空间')
center_window(root, 400, 230)
root.maxsize(300,115)
root.minsize(300,115)
win1 = Frame(root)
win2 = Frame(root)
win3 = Frame(root)

def denglu():
    Pro1_set(20)
    username = user.get()
    Pro1_set(40)
    Pass = password.get()
    Pro1_set(60)
    res = check_userpass(username,Pass)
    Pro1_set(800)
    if res == '成功':
        Pro1_set(100)
        time.sleep(0.5)
        root.destroy()
        import body
    else:
        Pro1_set(100)
        time.sleep(0.5)
        T = Toplevel(root)
        T.title('资源空间')
        center_window(T,100,50)
        Label(T,text='认证失败').pack()
        T.mainloop()
def denglu_2(self):
    denglu()
def zhuce():
    T = Toplevel(root)
    T.title('资源空间')
    center_window(T, 280, 50)
    Label(T, text='暂不提供注册\n请联系Email:mingserverwarning@gmial.com').pack()
    T.mainloop()
def Pro1_set(self):
    P1["value"]=self
    win4.update()
user = StringVar()
L1 = ttk.Label(win1,text='用户名')
en1 = ttk.Entry(win1,textvariable=user)
L1.grid(row=0,column=0)
en1.grid(row=0,column=1)
B1 = ttk.Button(win1,text='注册',command=zhuce)
B1.grid(row=0,column=2)
password = StringVar()
en2 = ttk.Entry(win2,textvariable=password)
en2['show']='*'
en2.bind('<Return>',denglu_2)
L2 = ttk.Label(win2,text='密   码')
L2.grid(row=0,column=0)
en2.grid(row=0,column=1)
B2 = ttk.Button(win2,text='登陆',command=denglu)
B2.grid(row=0,column=2)
win4 = Frame(root)
P1 = ttk.Progressbar(win4,length=280,mode="determinate",orient=HORIZONTAL)
P1.grid()
P1["maximum"]=100
P1["value"]=0

win1.grid(row=0,column=0,padx=12, pady=12)
win2.grid(row=1,column=0,padx=12, pady=2)
win3.grid(row=2,column=0,padx=1, pady=2)
win4.grid(row=3,column=0)
root.mainloop()