#coding:utf8
from tkinter import *
from tkinter import ttk
from use_mysql import *
import pymysql
import time
import re
import uuid
window = Tk()
Mysql_conn_config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'mysql_pass',
          'db':'auth',
          'charset':'utf8mb4',
          }
def center_window(tl, width, height):
    screenwidth = tl.winfo_screenwidth()
    screenheight = tl.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    tl.geometry(size)
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
def check_userpass(name, password):
    connection = pymysql.connect(**Mysql_conn_config)
    Pro_update(60)
    curr = connection.cursor()
    sql = "select pass from userdb where name='%s'" % name
    Pro_update(80)
    try:
        curr.execute(sql)
        Pro_update(90)
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
def check_all_usermac():
    connection = pymysql.connect(**Mysql_conn_config)
    Pro_update(60)
    curr = connection.cursor()
    sql = "select mac from userdb"
    try:
        curr.execute(sql)
        res = curr.fetchall()
        connection.close()
        return res
    except:
        connection.close()
        return '错误'
def check_login_mac(user_name):
    mac_num = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = "-".join([mac_num[e:e + 2] for e in range(0, 11, 2)])
    connection = pymysql.connect(**Mysql_conn_config)
    curr = connection.cursor()
    sql = "select mac from userdb where name='%s'"%user_name
    try:
        curr.execute(sql)
        res = curr.fetchall()
        if not res:
            return('失败')
            connection.close()
        elif res[0][0] == mac:
            return('成功')
            connection.close()
        else:
            return('失败')
            connection.close()
    except:
        connection.close()
        return('数据库错误')
def body():
    def flush_list():
        Pro_update(20)
        item = T1.get_children()
        for i in item:
            T1.delete(i)
        Pro_update(40)
        users = user_operating.select_alluser('aming', 'aming')
        num = 0
        Pro_update(60)
        for i in users:
            n = i[0]
            p = i[1]
            m = i[2]
            T1.insert("", num, text=num, values=(num, n, p, m))
            num = num + 1
        Pro_update(80)
        window.update()
        Pro_update(100)
        time.sleep(0.5)
        Pro_update(0)
    def add_Button():
        T = Toplevel(window)
        T.maxsize(260, 150)
        T.minsize(260, 150)
        center_window(T,260, 150)
        T.title('后台管理-添加用户')
        New_Add = Frame(T)
        info_1 = Label(New_Add, text='用户名')
        info_2 = Label(New_Add, text='输入密码')
        info_3 = Label(New_Add, text='重复密码')
        info_4 = Label(New_Add, text='MAC地址')
        username = StringVar()
        first_password = StringVar()
        second_password = StringVar()
        mac_zone = StringVar()
        name = ttk.Entry(New_Add, textvariable=username)
        password_1 = ttk.Entry(New_Add, textvariable=first_password)
        password_2 = ttk.Entry(New_Add, textvariable=second_password)
        mac_addr = ttk.Entry(New_Add, textvariable=mac_zone)
        Radio_button_zone = IntVar()
        Radio_1 = ttk.Radiobutton(New_Add, text='普通用户', variable=Radio_button_zone, value=0)
        Radio_2 = ttk.Radiobutton(New_Add, text='管理用户', variable=Radio_button_zone, value=1)
        Radio_button_zone.set(0)

        info_1.grid(row=0, column=0)
        info_2.grid(row=1, column=0)
        info_3.grid(row=2, column=0)
        info_4.grid(row=3, column=0)
        name.grid(row=0, column=1)
        def start_creat():
            Pro_update(20)
            Creat_user_name = username.get()
            Creat_user_mac = mac_zone.get()
            if password_1.get() == password_2.get():
                Creat_user_pass = password_1.get()
            else:
                T = Toplevel()
                T.title('资源空间')
                center_window(T, 280, 50)
                T.maxsize(280,50)
                T.minsize(280,50)
                Label(T, text='两次密码不一致').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                T.mainloop()
                return
            Pro_update(40)
            if Radio_button_zone.get() == 0:
                Creat_user_info = 'user'
            elif Radio_button_zone.get() == 1:
                Creat_user_info = 'admin_user'
            else:
                A = Toplevel()
                A.title('资源空间')
                center_window(A, 280, 50)
                A.maxsize(280, 50)
                A.minsize(280, 50)
                Label(A,text='用户类型错误').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                A.mainloop()
            if not re.search(u'^[_a-zA-Z0-9]+$', Creat_user_name):
                R = Toplevel()
                R.title('资源空间')
                center_window(R, 280, 50)
                R.maxsize(280,50)
                R.minsize(280,50)
                Label(R, text='用户名只能为数字或字母').pack()
                username.set('')
                first_password.set('')
                second_password.set('')
                Radio_button_zone.set(0)
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                R.mainloop()
                return
            connection = pymysql.connect(**Mysql_conn_config)
            curr = connection.cursor()
            sql = "insert into userdb(name,pass,info,mac) value('%s','%s','%s','%s')" % (Creat_user_name, Creat_user_pass, Creat_user_info,Creat_user_mac)
            sql2= "select name from userdb where name='%s'"%Creat_user_name
            try:
                curr.execute(sql2)
                res = curr.fetchall()
                if not res:
                    Pro_update(80)
                    try:
                        curr.execute(sql)
                        connection.commit()
                        S = Toplevel()
                        S.title('资源空间')
                        center_window(S, 280, 50)
                        S.maxsize(280, 50)
                        S.minsize(280, 50)
                        Label(S, text='创建成功').pack()
                        username.set('')
                        first_password.set('')
                        second_password.set('')
                        Radio_button_zone.set(0)
                        connection.close()
                        flush_list()
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                        S.mainloop()
                    except:
                        connection.close()
                        return
                else:
                    W = Toplevel()
                    W.title('资源空间')
                    center_window(W, 280, 50)
                    W.maxsize(280, 50)
                    W.minsize(280, 50)
                    Label(W, text='用户已存在').pack()
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
                    W.mainloop()
            except:
                return
        def start_creat_2(self):
            start_creat()
        Creat = ttk.Button(New_Add, text='创建', command=start_creat)
        Creat.bind('<Return>', start_creat_2)
        password_2.bind('<Return>', start_creat_2)
        password_1.grid(row=1, column=1)
        password_2.grid(row=2, column=1)
        mac_addr.bind('<Return>', start_creat_2)
        mac_addr.grid(row=3,column=1)
        Radio_1.grid(row=4, column=0)
        Radio_2.grid(row=4, column=1)
        Creat.grid(row=5, column=1)
        New_Add.grid(padx=20)
        T.mainloop()
    def del_user():
        Pro_update(40)
        res = T1.selection()
        if not T1.selection():
            T = Toplevel()
            T.title('资源空间')
            center_window(T, 310, 50)
            T.maxsize(310, 50)
            T.minsize(310, 50)
            Label(T,text='未选中任何用户').pack()
            Pro_update(100)
            time.sleep(0.5)
            Pro_update(0)
            T.mainloop()
            return
        else:
            for i in res:
                des_index = T1.item(i)['values'][0]
                des_value = T1.item(i)['values'][1]
                isadmin = user_operating.check_adminuser(des_value)
                if isadmin == '成功':
                    break
                else:
                    user_operating.delete_user('aming', 'aming', des_value)
            Pro_update(70)
            flush_list()
            Pro_update(100)
            time.sleep(0.5)
            Pro_update(0)
            return
    def select_user():
        T = Toplevel()
        T.title('资源空间')
        center_window(T, 310, 50)
        T.maxsize(310,50)
        T.minsize(310,50)
        L1 = Label(T,text='输入用户名')
        En_user = StringVar()
        E1 = ttk.Entry(T,textvariable=En_user)
        def select_all():
                Pro_update(20)
                if not En_user.get():
                    T = Toplevel()
                    T.title('资源空间')
                    center_window(T, 310, 50)
                    T.maxsize(310, 50)
                    T.minsize(310, 50)
                    Label(T, text='未选中任何用户').pack()
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
                    T.mainloop()
                    return
                else:
                    connection = pymysql.connect(**Mysql_conn_config)
                    curr = connection.cursor()
                    sql = "select pass from userdb where name='%s'" % En_user.get()
                    sql_2 = "select info from userdb where name='%s'" % En_user.get()
                    sql_3 = "select mac from userdb where name='%s'"% En_user.get()
                    Pro_update(60)
                    try:
                        curr.execute(sql)
                        pas = curr.fetchall()
                        curr.execute(sql_2)
                        useR = curr.fetchall()
                        curr.execute(sql_3)
                        Mac = curr.fetchall()
                        Pro_update(80)
                        if not pas or not useR:
                            D = Toplevel()
                            D.title('资源空间')
                            center_window(D, 280, 50)
                            D.maxsize(280, 50)
                            D.minsize(280, 50)
                            ttk.Label(D, text='无此用户').pack()
                            connection.close()
                            Pro_update(100)
                            time.sleep(0.5)
                            Pro_update(0)
                            connection.close()
                            D.mainloop()
                        else:
                            D = Toplevel()
                            D.title('资源空间')
                            center_window(D, 280, 60)
                            D.maxsize(280, 60)
                            D.minsize(280, 60)
                            Info = '该用户密码是:' + pas[0][0] + '，该用户标记为:' + useR[0][0]+'\n用户MAC为:'+Mac[0][0]
                            ttk.Label(D, text=Info).pack()
                            connection.close()
                            Pro_update(100)
                            time.sleep(0.5)
                            Pro_update(0)
                            D.mainloop()
                    except:
                        return ('无法连接数据库')
                        connection.close()
        def select_all_2(self):
                select_all()
        E1.bind('<Return>',select_all_2)
        B1 = ttk.Button(T,text='查找',command=select_all)
        B1.bind('<Return>',select_all_2)
        L1.grid(row=0,column=0)
        E1.grid(row=0,column=1)
        B1.grid(row=0,column=2)
        T.mainloop()
    def rename_user():
        def rename_oper():
            old_user = En1.get()
            new_user = En2.get()
            Pro_update(20)
            if old_user == new_user:
                Y = Toplevel()
                Y.title('资源空间')
                center_window(Y, 310, 50)
                Y.maxsize(310, 50)
                Y.minsize(310, 50)
                Label(Y, text='新旧用户名相同，无需修改').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                return
            connection = pymysql.connect(**Mysql_conn_config)
            curr = connection.cursor()
            Pro_update(40)
            check_sql = "select name from userdb where name='%s'"%old_user
            rename_sql = "update userdb set name='%s' where name='%s'"%(new_user,old_user)
            try:
                curr.execute(check_sql)
                res = curr.fetchall()
                Pro_update(60)
                if not res:
                    Y = Toplevel()
                    Y.title('资源空间')
                    center_window(Y, 310, 50)
                    Y.maxsize(310, 50)
                    Y.minsize(310, 50)
                    Label(Y,text='没有这个用户').pack()
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
                elif res[0][0] == old_user:
                    try:
                        curr.execute(rename_sql)
                        connection.commit()
                        G = Toplevel()
                        G.title('资源空间')
                        center_window(G, 310, 50)
                        G.maxsize(310, 50)
                        G.minsize(310, 50)
                        Label(G, text='修改成功').pack()
                        connection.close()
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                    except:
                        G = Toplevel()
                        G.title('资源空间')
                        center_window(G, 310, 50)
                        G.maxsize(310, 50)
                        G.minsize(310, 50)
                        Label(G, text='数据库错误').pack()
                        connection.close()
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                else:
                    curr.execute(rename_sql)
                    connection.commit()
                    G = Toplevel()
                    G.title('资源空间')
                    center_window(G, 310, 50)
                    G.maxsize(310, 50)
                    G.minsize(310, 50)
                    Label(G, text='程序错误').pack()
                    connection.close()
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
            except:
                curr.execute(rename_sql)
                connection.commit()
                G = Toplevel()
                G.title('资源空间')
                center_window(G, 310, 50)
                G.maxsize(310, 50)
                G.minsize(310, 50)
                Label(G, text='程序错误').pack()
                connection.close()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
        def rename_oper_2(self):
            rename_oper()
        F = Toplevel()
        F.title('资源空间')
        center_window(F, 200, 90)
        F.maxsize(200, 90)
        F.minsize(200, 90)
        old_name = StringVar()
        new_name = StringVar()
        L1 = Label(F,text='旧名称:')
        L2 = Label(F,text='新名称:')
        En1 = ttk.Entry(F,textvariable=old_name)
        En2 = ttk.Entry(F,textvariable=new_name)
        Bt = ttk.Button(F,text='更改',command=rename_oper)
        L1.grid(row=0,column=0)
        L2.grid(row=1,column=0)
        En1.grid(row=0,column=1)
        En2.grid(row=1,column=1)
        En2.bind('<Return>', rename_oper_2)
        Bt.grid(row=2,column=1,pady=10)
        Bt.bind('<Return>',rename_oper_2)
        F.mainloop()
    def repass_user():
        V = Toplevel()
        V.title('资源空间')
        center_window(V, 200, 100)
        V.maxsize(200, 100)
        V.minsize(200, 100)
        Label(V,text='用户名').grid(row=0,column=0)
        Label(V,text='新密码').grid(row=1,column=0)
        Label(V,text='新密码').grid(row=2,column=0)
        username = StringVar()
        first_pass = StringVar()
        second_pass = StringVar()
        Entry(V,textvariable=username).grid(row=0,column=1)
        Entry(V,textvariable=first_pass).grid(row=1,column=1)
        def repass_oper():
            if not username.get() or not first_pass.get() or not second_pass.get():
                T = Toplevel()
                T.title('资源空间')
                center_window(T, 310, 50)
                T.maxsize(310, 50)
                T.minsize(310, 50)
                Label(T, text='未选中任何用户').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                T.mainloop()
                return
            else:
                name = username.get()
                pass1 = first_pass.get()
                pass2 = second_pass.get()
                Pro_update(20)
                if pass1 == pass2:
                    connection = pymysql.connect(**Mysql_conn_config)
                    curr = connection.cursor()
                    check_sql = "select name from userdb where name='%s'"%name
                    rename_sql = "update userdb set pass='%s' where name='%s'"%(pass1,name)
                    Pro_update(40)
                    try:
                        curr.execute(check_sql)
                        res = curr.fetchall()
                        Pro_update(60)
                        if not res:
                            B = Toplevel()
                            B.maxsize(100, 50)
                            B.minsize(100, 50)
                            center_window(B, 100, 50)
                            text = '无此用户'
                            Label(B, text=text).pack()
                            connection.close()
                            Pro_update(100)
                            time.sleep(0.5)
                            Pro_update(0)
                            B.mainloop()
                        elif res[0][0] == name:
                            try:
                                curr.execute(rename_sql)
                                connection.commit()
                                Pro_update(80)
                                T = Toplevel()
                                T.maxsize(100, 50)
                                T.minsize(100, 50)
                                center_window(T, 100, 50)
                                Label(T, text='修改成功').pack()
                                connection.close()
                                username.set('')
                                first_pass.set('')
                                second_pass.set('')
                                Pro_update(100)
                                time.sleep(0.5)
                                Pro_update(0)
                                T.mainloop()
                            except:
                                C= Toplevel()
                                C.maxsize(100, 50)
                                C.minsize(100, 50)
                                center_window(C, 300, 50)
                                text = '数据库错误'
                                Label(C, text=text).pack()
                                connection.close()
                                Pro_update(100)
                                time.sleep(0.5)
                                Pro_update(0)
                                C.mainloop()
                    except:
                        T = Toplevel()
                        T.maxsize(100, 50)
                        T.minsize(100, 50)
                        center_window(T, 100, 50)
                        text = '数据库错误'
                        Label(T, text=text).pack()
                        connection.close()
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                        T.mainloop()
                else:
                    T = Toplevel(window)
                    T.maxsize(150, 50)
                    T.minsize(150, 50)
                    center_window(T, 150, 50)
                    Label(T,text='两次密码不相同,请重新输入').pack()
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
                    T.mainloop()
        def repass_oper_2(self):
                repass_oper()
        secpas = Entry(V,textvariable=second_pass)
        secpas.bind('<Return>',repass_oper_2)
        secpas.grid(row=2,column=1)
        B1 = ttk.Button(V,text='修改',command=repass_oper)
        B1.grid(row=4,column=1)
        B1.bind('<Return>',repass_oper_2)
        V.mainloop()
    def remac_user():
        G = Toplevel()
        G.title('资源空间')
        center_window(G, 220, 100)
        G.maxsize(220, 120)
        G.minsize(220, 120)
        Label(G,text='用户名:').grid(row=0,column=0,padx=8,pady=5)
        Label(G,text='新MAC:').grid(row=1,column=0,padx=8,pady=5)
        uname = StringVar()
        umac = StringVar()
        Uname = ttk.Entry(G,textvariable=uname)
        Umac = ttk.Entry(G,textvariable=umac)
        def remac_oper():
            if not uname.get() or not umac.get():
                T = Toplevel()
                T.title('资源空间')
                center_window(T, 310, 50)
                T.maxsize(310, 50)
                T.minsize(310, 50)
                Label(T, text='未选中任何用户').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                T.mainloop()
                return
            else:
                Pro_update(20)
                connection = pymysql.connect(**Mysql_conn_config)
                curr = connection.cursor()
                check_u = "select name from userdb where name='%s'"%uname.get()
                remac = "update userdb set mac='%s' where name='%s'"%(umac.get(),uname.get())
                Pro_update(40)
                try:
                    curr.execute(check_u)
                    res = curr.fetchall()
                    Pro_update(60)
                    if not res:
                        Y = Toplevel()
                        Y.title('资源空间')
                        center_window(Y, 220, 100)
                        Y.maxsize(220, 120)
                        Y.minsize(220, 120)
                        Label(Y,text='无此用户').pack()
                        connection.close()
                        uname.set('')
                        umac.set('')
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                        Y.mainloop()
                    elif res[0][0] == uname.get():
                        try:
                            curr.execute(remac)
                            connection.commit()
                            Pro_update(80)
                            Y = Toplevel()
                            Y.title('资源空间')
                            center_window(Y, 220, 100)
                            Y.maxsize(220, 120)
                            Y.minsize(220, 120)
                            Label(Y, text='更改成功').pack()
                            connection.close()
                            Pro_update(100)
                            time.sleep(0.5)
                            Pro_update(0)
                            Y.mainloop()
                            return
                        except:
                            Y = Toplevel()
                            Y.title('资源空间')
                            center_window(Y, 220, 100)
                            Y.maxsize(220, 120)
                            Y.minsize(220, 120)
                            Label(Y, text='更改失败').pack()
                            connection.close()
                            uname.set('')
                            umac.set('')
                            Pro_update(100)
                            time.sleep(0.5)
                            Pro_update(0)
                            Y.mainloop()
                            return
                    else:
                        Y = Toplevel()
                        Y.title('资源空间')
                        center_window(Y, 220, 100)
                        Y.maxsize(220, 120)
                        Y.minsize(220, 120)
                        Label(Y, text='更改失败').pack()
                        connection.close()
                        uname.set('')
                        umac.set('')
                        Pro_update(100)
                        time.sleep(0.5)
                        Pro_update(0)
                        Y.mainloop()
                        return
                except:
                    Y = Toplevel()
                    Y.title('资源空间')
                    center_window(Y, 220, 100)
                    Y.maxsize(220, 120)
                    Y.minsize(220, 120)
                    Label(Y, text='更改失败').pack()
                    connection.close()
                    uname.set('')
                    umac.set('')
                    Pro_update(100)
                    time.sleep(0.5)
                    Pro_update(0)
                    Y.mainloop()
                    return
        def remac_oper_2(self):
                remac_oper()
        Bu1 = ttk.Button(G,text='更改',command=remac_oper)
        Bu1.bind('<Return>',remac_oper_2)
        Umac.bind('<Return>',remac_oper_2)
        Uname.grid(row=0,column=1,padx=1,pady=5)
        Umac.grid(row=1,column=1,padx=1,pady=5)
        Bu1.grid(row=2,column=1,padx=1,pady=5)
        G.mainloop()
    def readme():
        r = Toplevel()
        r.title('资源空间')
        center_window(r, 300, 80)
        r.maxsize(300, 80)
        r.minsize(300, 80)
        Label(r,text='鼠标点击选中用户列表中的用户，\n或者使用Ctrl和Shift键多选然后点击删除用户\n即可将选中的用户全部删除,\n注意: 用户的MAC地址一定要小写！！！').pack()
        r.mainloop()
    Tab = Frame(window)
    Lab = Label(Tab, text='用户列表:')
    Lab.grid(row=0, column=0)
    T1 = ttk.Treeview(Tab, height=12, show="headings")
    T1["column"] = ('ID', '用户','密码','MAC')
    T1.column('用户', width='90')
    T1.column('ID', width='30')
    T1.column('密码',width='90')
    T1.column('MAC',width='150')
    T1.heading('MAC',text='MAC')
    T1.heading('密码',text='密码')
    T1.heading('ID', text='ID')
    T1.heading('用户', text='用户')
    users = user_operating.select_alluser('aming', 'aming')
    num = 0
    for i in users:
        n = i[0]
        p = i[1]
        m = i[2]
        T1.insert("", num, text=num, values=(num,n,p,m))
        num = num + 1
    Bar = ttk.Scrollbar(Tab, orient=VERTICAL, command=T1.yview)
    T1.configure(yscrollcommand=Bar.set)
    Bar.grid(row=1, column=1, sticky=NS)
    T1.grid(row=1, column=0)

    But1 = Frame(window)
    b1 = ttk.Button(But1, text='添加用户', command=add_Button)
    b2 = ttk.Button(But1, text='删除用户', command=del_user)
    b3 = ttk.Button(But1, text='查找用户', command=select_user)
    b4 = ttk.Button(But1, text='用户改MAC', command=remac_user)
    b5 = ttk.Button(But1, text='用户改名', command=rename_user)
    b6 = ttk.Button(But1, text='用户改密', command=repass_user)
    b7 = ttk.Button(But1, text='刷新列表', command=flush_list)
    b8 = ttk.Button(But1, text='使用说明', command=readme)
    b1.grid(row=0, column=0, pady=6)
    b2.grid(row=1, column=0, pady=6)
    b3.grid(row=2, column=0, pady=6)
    b4.grid(row=3, column=0, pady=6)
    b5.grid(row=4, column=0, pady=6)
    b6.grid(row=5, column=0, pady=6)
    b7.grid(row=6, column=0, pady=6)
    b8.grid(row=7, column=0, pady=6)

    But1.grid(row=1, column=0, padx=10)
    Tab.grid(row=1, column=1, padx=12)
def Pro_update(self):
    Pro["value"]=self
    window.update()
def denglu_button():
    Pro_update(20)
    if not En1_zone.get() or not En2_zone.get():
        Pro_update(100)
        T = Toplevel(window)
        T.title('资源空间')
        center_window(T, 150, 40)
        T.maxsize(150,40)
        T.minsize(150,40)
        Label(T, text='请输入完整用户名和密码').pack()
        Pro_update(100)
        time.sleep(0.5)
        Pro_update(0)
        T.mainloop()
        return
    else:
        Pro_update(40)
        res = check_userpass(En1_zone.get(), En2_zone.get())
        if res == '成功':
            auth = check_adminuser(En1_zone.get())
            if auth == '成功':
                Fra.destroy()
                body()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                return
            else:
                T = Toplevel(window)
                T.title('资源空间')
                center_window(T, 100, 50)
                T.maxsize(150, 40)
                T.minsize(150, 40)
                Label(T, text='请使用管理员账户登陆').pack()
                Pro_update(100)
                time.sleep(0.5)
                Pro_update(0)
                T.mainloop()
                return
        else:
            T = Toplevel(window)
            T.title('资源空间')
            center_window(T, 100, 50)
            T.maxsize(150, 40)
            T.minsize(150, 40)
            Label(T, text='用户名或密码错误').pack()
            Pro_update(100)
            time.sleep(0.5)
            Pro_update(0)
            T.mainloop()
            return
def denglu_enter(self):
    denglu_button()
center_window(window,530,350)
window.title('后台管理')
window.maxsize(530,350)
window.minsize(530,350)
Fra = Frame(window,bg='#FFC')
win1 = Frame(Fra)
win2 = Frame(Fra)
win3 = Frame(Fra)
L1 = Label(win1,text='管理员账号:',bg='#FFC')
L2 = Label(win2,text='管理员密码:',bg='#FFC')
En1_zone=StringVar()
En2_zone=StringVar()
E1 = ttk.Entry(win1,textvariable=En1_zone)
E2 = ttk.Entry(win2,textvariable=En2_zone,show='*')
B1 = ttk.Button(win3,text='登陆',command=denglu_button)
L1.grid(row=0,column=0)
L2.grid(row=0,column=0)
E1.grid(row=0,column=1)
E2.grid(row=0,column=1)
E2.bind("<Return>",denglu_enter)
B1.grid(row=0,column=0)
B1.bind("<Return>",denglu_enter)
Pro = ttk.Progressbar(window,length=530,mode="determinate",orient=HORIZONTAL)
Pro.place(y=330)
Pro["maximum"]=100
Pro["value"]=0
win1.grid(padx=125,pady=20)
win2.grid(padx=165)
win3.grid(padx=185,pady=10)
Fra.place(y=100)
window.mainloop()