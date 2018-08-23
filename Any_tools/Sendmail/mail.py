#coding:utf8
from email.mime.text import MIMEText
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mBox
import smtplib,threading,re,os


class Application():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('%dx%d+%d+%d' % (699, 500, (self.root.winfo_screenwidth() - 700) / 2, (self.root.winfo_screenheight() - 700) / 2))
        self.root.maxsize(699,500)
        self.root.minsize(699,500)
        self.root.title('邮件助手')
        self.tk_body()
    def check_user_pass(self):
        self.content_text.insert(END,'--> 正在验证用户密码是否可用\n')
        self.content_text.update()
        self.mailto_list = ['mingserverwarning@gmail.com',]
        self.me = self.user_en.get()  # 发件人
        self.mail_host = self.red_group.get()  # 邮箱服务器
        self.mail_user = self.user_en.get()  # 登录服务器的用户名
        self.mail_pass = self.pass_en.get()  # qq授权码

        msg = MIMEText('测试正文')  # 初始化 mime对象
        msg['Subject'] = '测试标题'  # 邮件标题
        msg['From'] = self.me  # 从哪里发 发件地址
        msg['To'] = ';'.join(self.mailto_list)  # 发到哪里
        def threa_send_mail():
            for to in self.mailto_list:
                try:
                    s = smtplib.SMTP_SSL(self.mail_host, 465)  # 初始化stmp_ssl 对象   465邮件服务器端口
                    s.connect(self.mail_host)  # 连接stmp邮件服务器
                    s.login(self.mail_user, self.mail_pass)  # 登陆smtp服务器 用qq号 和  授权码登陆
                    s.sendmail(self.me, to, msg.as_string())  # 登陆成功  发送邮件
                    s.close()  # 关闭smtp 连接
                    self.content_text.insert(END,'--> '+'验证成功\n')
                except Exception as e:
                    mBox.showerror('连接失败','连接失败，请检查网络连接和密码\n'+str(e))
        send_mail_thr = threading.Thread(target=threa_send_mail)
        send_mail_thr.start()
    def start_send_mail(self):
        if self.user_list_text.get(0.0,END) == '\n' or not self.info_en_str.get() or self.mail_body_text.get(0.0,END) == '\n':
            mBox.showinfo('提示','请完善收件人或标题正文信息')
        else:
            self.content_text.insert(END,'--> 正在执行发送指令,请稍后\n')
            send_list = re.split(r'\n',self.user_list_text.get(0.0,END))
            self.mailto_list = send_list
            self.me = self.user_en.get()  # 发件人
            self.mail_host = self.red_group.get()  # 邮箱服务器
            self.mail_user = self.user_en.get()  # 登录服务器的用户名
            self.mail_pass = self.pass_en.get()  # qq授权码
            msg = MIMEText(self.mail_body_text.get(0.0,END))  # 初始化 mime对象
            msg['Subject'] = self.info_en_str.get()  # 邮件标题
            msg['From'] = self.me  # 从哪里发 发件地址
            msg['To'] = ';'.join(self.mailto_list)  # 发到哪里
            def threa_send_mail():
                for to in self.mailto_list:
                    if not to:
                        continue
                    else:
                        try:
                            s = smtplib.SMTP_SSL(self.mail_host, 465)  # 初始化stmp_ssl 对象   465邮件服务器端口
                            s.connect(self.mail_host)  # 连接stmp邮件服务器
                            s.login(self.mail_user, self.mail_pass)  # 登陆smtp服务器 用qq号 和  授权码登陆
                            s.sendmail(self.me, to, msg.as_string())  # 登陆成功  发送邮件
                            s.close()  # 关闭smtp 连接
                            self.content_text.insert(END,'--> '+'成功:'+to+'\n')
                        except Exception as e:
                            mBox.showerror('连接失败','连接失败，请检查网络连接和密码\n'+str(e))
                self.content_text.insert(END,'--> 本次发送已全部完成\n')
            send_mail_thr = threading.Thread(target=threa_send_mail)
            send_mail_thr.start()
    def flush_all(self):
        self.mail_body_text.delete(0.0,END)
        self.user_list_text.delete(0.0,END)
        self.info_en_str.set('')
        self.content_text.delete(0.0,END)
        self.root.update()
    def tk_body(self):
        self.frame = Frame(self.root, width=700, height=500, bg='#708090')
        self.from_fra = Frame(self.frame, width=459, height=128, bg='#FFC')
        Label(self.frame,text='发件人信息:', bg='#FFC',fg='blue').place(x=120,y=10)
        Label(self.frame,text='SMTP服务器:', bg='#FFC',fg='blue').place(x=350,y=10)
        self.user_en_str = StringVar()
        self.pass_en_str = StringVar()
        def flush_user_entry(se):
            if self.first_user_en_click == 0:
                self.user_en_str.set('')
                self.first_user_en_click = 1
                return
            else:
                return
        def flush_pass_entry(se):
            if self.first_pass_en_click == 0:
                self.pass_en_str.set('')
                self.first_pass_en_click = 1
                return
            else:
                return
        self.user_en = ttk.Entry(self.from_fra,width=28,textvariable=self.user_en_str)
        self.first_user_en_click = 0
        self.first_pass_en_click = 0
        self.user_en.bind("<Button-1>",flush_user_entry)
        self.pass_en = ttk.Entry(self.from_fra,width=28,textvariable=self.pass_en_str,show='*')
        self.pass_en.bind("<Button-1>", flush_pass_entry)
        self.user_en_str.set('mingserverwarning@gmail.com')
        self.pass_en_str.set('0.00..000...')
        Label(self.from_fra, text='用户:', bg='#FFC').place(x=15, y=40)
        Label(self.from_fra, text='密码:', bg='#FFC').place(x=15, y=70)
        Label(self.from_fra, text='注:此密码为SMTP邮箱服务器的认证密码,如QQ、163都有独立的SMTP密码', bg='#FFC').place(x=10, y=98)
        check_but = ttk.Button(self.from_fra, text='检查密码',command=self.check_user_pass)
        enter_but = ttk.Button(self.from_fra, text='确认登陆')
        style = ttk.Style()
        style.configure("C.TRadiobutton", background="#FFC", foreground="black")
        self.red_group = StringVar()
        self.red1 = ttk.Radiobutton(self.from_fra,text='google邮箱',style="C.TRadiobutton",variable=self.red_group,value='smtp.gmail.com')
        self.red2 = ttk.Radiobutton(self.from_fra,text='163邮箱',style="C.TRadiobutton",variable=self.red_group,value='smtp.qq.com')
        self.red_group.set('smtp.gmail.com')
        self.red1.place(x=350,y=40)
        self.red2.place(x=350,y=70)
        check_but.place(x=255, y=38)
        enter_but.place(x=255, y=68)
        self.user_en.place(x=50, y=40)
        self.pass_en.place(x=50, y=70)
#       ================================================================================================================
        self.update_ip = Frame(self.frame,width=240,height=128)
        pwd = os.getcwd()
        img_frame = Frame(self.update_ip, height=126, width=238)
        bm = PhotoImage(file=pwd + '\\tp.png')
        label1 = Label(img_frame, image=bm)
        label1.bm = bm
        label1.place(x=0,y=0)
        img_frame.place(x=0,y=0)
#       ================================================================================================================
        self.info_fra = Frame(self.frame, width=239, height=369, bg='#BDE')
        Label(self.info_fra,text='邮件内容设定',bg='#BDE',fg='blue').place(x=80,y=10)
        self.info_en_str = StringVar()
        Label(self.info_fra, text='邮件标题:',bg='#BDE').place(x=10,y=40)
        self.info_en = ttk.Entry(self.info_fra,width=20,textvariable=self.info_en_str)
        self.mail_body_text = Text(self.info_fra,width=20,height=17)
        Label(self.info_fra,text='邮件正文:',bg='#BDE').place(x=10,y=70)
        self.flash_button = ttk.Button(self.info_fra,text='清空',command=self.flush_all)
        self.send_button = ttk.Button(self.info_fra,text='发送',command=self.start_send_mail)
        self.flash_button.place(x=25,y=325)
        self.send_button.place(x=130,y=325)
        self.info_en.place(x=70,y=40)
        self.mail_body_text.place(x=70,y=70)
#       ================================================================================================================
        self.content_fra = Frame(self.frame, width=250, height=369, bg='#EDC')
        self.content_text = Text(self.content_fra, width=35, height=25, bg='#EDC')
        Label(self.content_fra, text='状态信息', bg='#EDC',fg='blue').place(x=100, y=10)
        self.content_text.place(x=0, y=40)
#       ================================================================================================================
        self.user_list_fra = Frame(self.frame, width=208, height=369, bg='#CDC')
        self.user_list_text = Text(self.user_list_fra, width=35, height=25, bg='#CDC')
        Label(self.user_list_fra,text='收件人列表,每行一个',bg='#CDC',fg='blue').place(x=45,y=10)
        self.user_list_text.place(x=0, y=40)
#       ================================================================================================================
        self.from_fra.place(x=0, y=1)
        self.update_ip.place(x=460,y=1)
        self.info_fra.place(x=460, y=130)
        self.content_fra.place(x=0, y=130)
        self.user_list_fra.place(x=251, y=130)
        self.frame.grid()
        self.root.mainloop()


if __name__ == '__main__':
    Application()