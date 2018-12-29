
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re

class app():
    def __init__(self):
        self.root = Tk()
        self.root.maxsize(900, 500)
        self.root.minsize(900, 500)
        # self.root.iconbitmap(".\\kingd.ico")
        self.root.geometry('%dx%d+%d+%d' % (
        900, 500, (self.root.winfo_screenwidth() - 900) / 2, (self.root.winfo_screenheight() - 900) / 2))
        self.root.title('王朝国际Nginx证书配置生成器 v1.0')
        self.domain_list_frame()
        self.but_frame()
        self.www_frame()
        self.m_frame()
        self.root.mainloop()
    def clicked(self):
        res = self.domain_text.get(0.0,END)
        for s in res.split("\n"):
            if s == "":
                continue
            else:
                if len(re.split(r'\.',s)) != 2:
                    messagebox.showerror('Error','域名列表错误')
                else:
                    self.m_conf_insert(s,self.crt_pos.get())
                    self.pc_conf_insert(s,self.crt_pos.get())
    def pc_conf_insert(self,dn,ssl_url):
        pc_text = str("server {\nlisten 80;\nlisten 443 ssl;\nserver_name ") + str(dn) + str(" www.") + str(dn) + str(
            ";\nssl_certificate ") + str(ssl_url) + str("1_") + str(dn) + str(
            "_bundle.crt;\nssl_certificate_key ") + str(ssl_url) + str("2_") + str(dn) + str(
            ".key;\ncharset UTF-8;\naccess_log logs/new_access.log access_cookie;\nproxy_http_version 1.1;\nproxy_set_header Host $http_host;\nproxy_set_header Connection \"\";\nproxy_set_header X-Real-IP $http_x_real_ip;\nproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\nif ($scheme = http ) {return 301 https://$host$request_uri;}\nlocation / {\nroot  /home/waguda/web/cash;\nindex index.html;\ntry_files $uri $uri/ /index.html =404;\nexpires 1d;\nbreak;}\nlocation ^~ /d/{\nproxy_pass http://cash_prod_webserver;\nbreak;}\n}")
        self.www_text.insert(END, pc_text + "\n")
    def m_conf_insert(self,dn,ssl_url):
        m_text = str("server {\nlisten 80;\nlisten 443 ssl;\nserver_name m.") + str(dn) + str(
            ";\nssl_certificate ") + str(ssl_url) + str("1_m.") + str(dn) + str(
            "_bundle.crt;\nssl_certificate_key ") + str(ssl_url) + str("2_m.") + str(dn) + str(
            ".key;\ncharset UTF-8;\naccess_log logs/new_access.log access_cookie;\nproxy_http_version 1.1;\nproxy_set_header Host $http_host;\nproxy_set_header Connection "";\nproxy_set_header X-Real-IP $http_x_real_ip;\nproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\nif ($scheme = http ) {return 301 https://$host$request_uri;}\nlocation / {\nroot  /home/waguda/web/cashsmart;\nindex index.html;\ntry_files $uri $uri/ /index.html =404;\nexpires 1d;\nbreak;}\nlocation ^~ /old/ {\nroot  /home/waguda/web/cashsmart;\nindex index.html;\ntry_files $uri $uri/ /old/index.html =404;\nbreak;}\nlocation ^~ /d/{\nproxy_pass http://cash_prod_webserver;\nbreak;}\n}")
        self.m_text.insert(END,m_text + "\n")
    def domain_list_frame(self):
        config_Frame = Frame(self.root, width=450,height=150)
        Label(config_Frame,text="输入主域名列表，不要www和m").pack()
        self.domain_text = Text(config_Frame,width=60, height=9)
        sc = Scrollbar(config_Frame)
        sc.config(command=self.domain_text.yview)
        self.domain_text.config(yscrollcommand=sc.set)
        sc.pack(side=RIGHT, fill=Y)
        self.domain_text.pack()
        config_Frame.place(x=0,y=0)
    def but_frame(self):
        but_Frame = Frame(self.root,width=450,height=150)
        Label(but_Frame, text="证书文件位置:").place(x=0,y=30)
        self.crt_text = StringVar(value="/usr/local/nginx/ssl/dn/")
        self.crt_pos = ttk.Entry(but_Frame,textvariable=self.crt_text,width=40)
        self.crt_pos.place(x=100,y=30)
        self.click = ttk.Button(but_Frame,text="Go!!!",command=self.clicked)
        self.click.place(x=175,y=100)
        but_Frame.place(x=450,y=0)
    def www_frame(self):
        www_Frame = Frame(self.root, width=450, height=350)
        Label(www_Frame, text="www和@配置文件内容:").pack()
        self.www_text = Text(www_Frame, width=60, height=24)
        sc = Scrollbar(www_Frame)
        sc.config(command=self.www_text.yview)
        self.www_text.config(yscrollcommand=sc.set)
        sc.pack(side=RIGHT, fill=Y)
        self.www_text.pack()
        www_Frame.place(x=0,y=150)
    def m_frame(self):
        m_Frame = Frame(self.root, width=450, height=350)
        Label(m_Frame, text="m配置文件内容:").pack()
        self.m_text = Text(m_Frame, width=60, height=24)
        sc = Scrollbar(m_Frame)
        sc.config(command=self.m_text.yview)
        self.m_text.config(yscrollcommand=sc.set)
        sc.pack(side=RIGHT, fill=Y)
        self.m_text.pack()
        m_Frame.place(x=450,y=150)

if __name__ == '__main__':
    app()