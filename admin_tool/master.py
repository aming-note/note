#coding:utf8
from tkinter import *
from tkinter import ttk
import requests,json,threading,re
class app():
    def __init__(self):
        self.root = Tk()
        self.root.maxsize(600,500)
        self.root.minsize(600,500)
        # self.root.iconbitmap(".\\kingd.ico")
        self.root.geometry('%dx%d+%d+%d' % (600, 500, (self.root.winfo_screenwidth() - 600) / 2, (self.root.winfo_screenheight() - 600) / 2))
        self.root.title('Made In China')
        self.but()
        self.text_mode()
        self.root.mainloop()
    def onclick(self):
        if self.val.get() == 1 and self.name_en.get() and self.times.get():
            if self.dl.get() == 1:
                self.add_user(self.name_en.get(),self.dl_name.get())
            else:
                self.add_user(self.name_en.get(), "null")
        elif self.val.get() == 2 and self.tocken_group.get() and self.agent_en.get():
            if self.dl.get() == 1:
                self.add_agent(self.agent_en.get(),self.times.get(),self.tocken_group.get(),self.dl_name.get())
            else:
                self.add_agent(self.agent_en.get(), self.times.get(),self.tocken_group.get(), "null")
        else:
            self.print_info('参数错误')
    def click_thread(self):
        t1 = threading.Thread(target=self.onclick)
        t1.start()
    def add_user(self,user_name,agent):
        url = "http://www.kingdomuat.com/d/member/register"
        if self.times_group.get():
            for i in range(0,int(self.times_group.get())):
                if agent != "null":
                    self.print_info('正在创建第%s个用户%s，代理%s'%(i,user_name,agent))
                    data = "data="+str(json.dumps({"UserName":"%s%s"%(user_name,i),"Password":"qwe123","SecurePassword":"123123","SureName":"李狗蛋","PromoCode":"%s"%(agent)}))
                    try:
                        res = requests.post(url,data)
                        if re.split('"', re.split(':', re.split(',', str(res.text))[0])[1])[1] == "NoError":
                            self.print_info("创建成功")
                        else:
                            self.print_info("创建失败,错误：%s" % (res.text))
                    except Exception as e:
                        self.print_info("%s"%(e))
                else:
                    self.print_info('正在创建第%s个用户%s，无代理'%(i,user_name))
                    data = "data=" + str(json.dumps({"UserName": "%s%s" % (user_name,i), "Password": "qwe123", "SecurePassword": "123123", "SureName": "李狗蛋"}))
                    try:
                        res = requests.post(url, data)
                        if re.split('"', re.split(':', re.split(',', str(res.text))[0])[1])[1] == "NoError":
                            self.print_info("创建成功")
                        else:
                            self.print_info("创建失败,错误：%s"%(res.text))
                    except Exception as e:
                        self.print_info("%s"%(e))
        else:
            self.print_info('参数错误')
    def add_agent(self,agent_name,times,tocken,agent):
        url = "http://www.kingdomuat.com/d/agent/register"
        if self.times_group.get():
            for a in range(0,int(self.times_group.get())):
                if agent != "null":
                    data = "data=" + str(json.dumps(
                        {"UserName": "%s%s"%(agent_name,a), "Password": "qwe123", "SecurePassword": "123123", "SureName": "李狗蛋",
                         "Mobile": "15478945612", "Email": "amingworkmail@gmail.com", "QQ": "4008123123", "Wechat": "wx5481267",
                         "PromoCode":"%s"%(agent),"BankName": "ICBC", "BankAddress": "天地银行", "BankAccountNo": "40005187934315486"}))
                    try:
                        res = requests.post(url, data)
                        self.print_info('正在创建第%s个代理%s，数量%s，上级代理%s'%(a,agent_name,times,agent))
                        if re.split('"', re.split(':', re.split(',', str(res.text))[0])[1])[1] == "NoError":
                            self.print_info("创建成功")
                            self.enable_agent("%s%s"%(agent_name,a),tocken)
                        else:
                            self.print_info("创建失败,错误：%s" % (res.text))
                    except Exception as e:
                        self.print_info("%s"%(e))
                else:
                    data = "data=" + str(json.dumps(
                        {"UserName": "%s%s" % (agent_name, a), "Password": "qwe123", "SecurePassword": "123123",
                         "SureName": "李狗蛋","Mobile": "15478945612", "Email": "amingworkmail@gmail.com", "QQ": "4008123123",
                         "Wechat": "wx5481267","BankName": "ICBC", "BankAddress": "天地银行","BankAccountNo": "40005187934315486"}))
                    try:
                        res = requests.post(url, data)
                        self.print_info('正在创建第%s个代理%s，数量%s，无上级代理'%(a,agent_name,times))
                        if re.split('"', re.split(':', re.split(',', str(res.text))[0])[1])[1] == "NoError":
                            self.print_info("创建成功")
                            self.enable_agent("%s%s" % (agent_name, a), tocken)
                        else:
                            self.print_info("创建失败,错误：%s" % (res.text))
                    except Exception as e:
                        self.print_info("%s"%(e))
        else:
            self.print_info('参数错误')
    def enable_agent(self,agent_name,tocken):
        url = "http://admin.cashlotteryuat.com/d/agent/updatestatus"
        data = "data=" + str(json.dumps(
            {"UserName": "kingd.%s"%(agent_name), "Status": "Enable"}))
        headers = {"Host": "admin.cashlotteryuat.com",
                   "Connection": "keep-alive",
                   "Content-Length": "82",
                   "Accept": "application/json, text/plain, */*",
                   "Origin": "http://admin.cashlotteryuat.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Referer": "http://admin.cashlotteryuat.com/admin/agentList",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Cookie": "%s" % (tocken)}
        try:
            res = requests.post(url,data,headers=headers)
            if re.split('"', re.split(':', re.split(',', str(res.text))[0])[1])[1] == "NoError":
                self.print_info("审核成功")
            else:
                self.print_info("审核失败,错误：%s" % (res.text))
        except Exception as e:
            self.print_info("%s" % (e))
    def print_info(self,info):
        self.text.insert(END, info+'\n')
        self.text.see(END)
    def but(self):
        win1 = Frame(self.root,width=600,height=300)
        go = ttk.Button(win1,text='Go!!!',command=self.click_thread)
        go.place(x=260,y=260)
        self.val = IntVar()
        def add_user():
            self.name_en.config(state='write')
            self.agent_en.config(state='readonly')
            self.tocken.config(state='readonly')
            self.tocken_group.set(value='创建用户无需tocken')
            self.agentname.set(value='')
            self.dl_ra1.place(x=430,y=14)
            self.dl_ra2.place(x=430,y=34)
            self.dl_name.place(x=480, y=23)
            dl_lb.place(x=330,y=23)
            self.lb_group.set('是否所属代理？')
        def add_agent():
            self.name_en.config(state='readonly')
            self.agent_en.config(state='write')
            self.tocken.config(state='write')
            self.tocken_group.set(value='')
            self.username.set(value='')
            self.dl_ra1.place(x=430, y=14)
            self.dl_ra2.place(x=430, y=34)
            self.dl_name.place(x=480, y=23)
            dl_lb.place(x=330, y=23)
            self.lb_group.set('是否有上级代理？')
        # ==========================================================================================================
        ttk.Radiobutton(win1,text='创建用户',variable=self.val,value=1,command=add_user).place(x=250,y=10)
        Label(win1,text="用户名称前缀").place(x=10,y=10)
        self.username = StringVar()
        self.name_en = ttk.Entry(win1,textvariable=self.username,state='readonly')
        self.name_en.place(x=100, y=10)
        self.dl = IntVar()
        def check_dl_y():
            self.dl_name.config(state='write')
            self.dl_group.set('')
        def check_dl_n():
            self.dl_group.set('请输入代理code')
            self.dl_name.config(state='readonly')
        self.lb_group = StringVar()
        dl_lb = Label(win1,textvariable=self.lb_group)
        self.dl_ra1 = ttk.Radiobutton(win1,text='是',variable=self.dl,value=1,command=check_dl_y)
        self.dl_ra2 = ttk.Radiobutton(win1,text='否',variable=self.dl,value=2,command=check_dl_n)
        self.dl_group = StringVar()
        self.dl_name = ttk.Entry(win1,textvariable=self.dl_group,width=15,state='readonly')
        self.dl_group.set('请输入代理code')
        # ==========================================================================================================
        ttk.Radiobutton(win1, text='创建代理', variable=self.val, value=2, command=add_agent).place(x=250, y=35)
        Label(win1, text="代理名称前缀").place(x=10, y=35)
        self.agentname = StringVar()
        self.agent_en = ttk.Entry(win1, textvariable=self.agentname,state='readonly')
        self.agent_en.place(x=100, y=35)
        # ==========================================================================================================
        Label(win1, text="Tocken").place(x=10, y=60)
        self.tocken_group = StringVar(win1)
        self.tocken = ttk.Entry(win1, textvariable=self.tocken_group)
        self.tocken.place(x=100, y=60)
        # ==========================================================================================================
        Label(win1, text="创建数量").place(x=10, y=85)
        self.times_group = StringVar(win1,value=10)
        self.times = ttk.Entry(win1,textvariable=self.times_group,width=5)
        self.times.place(x=100,y=85)
        win1.pack()
    def text_mode(self):
        win2 = Frame(self.root,width=600,height=200,bg='blue')
        self.text = Text(win2,width=85,height=15)
        sc = Scrollbar(win2)
        sc.config(command=self.text.yview)
        self.text.config(yscrollcommand=sc.set)
        sc.pack(side=RIGHT, fill=Y)
        self.text.pack()
        win2.pack()
if __name__ == '__main__':
    app()