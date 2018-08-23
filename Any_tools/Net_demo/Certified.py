#coding:utf8
import time,os
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('%dx%d+%d+%d' % (665, 500, (root.winfo_screenwidth() - 665) / 2, (root.winfo_screenheight() - 665) / 2))
root.title('Server Manager')
pwd = os.getcwd()
root.maxsize(665,500)
root.minsize(665,500)
logo = PhotoImage(file=pwd+'\\logo.gif')
root.tk.call('wm','iconphoto',root._w,logo)
img_frame=Frame(root,height=100,width=100)
bm = PhotoImage(file=pwd+'\\rw1.png')
label1 = Label(img_frame,image=bm,bg='#AFD')
label1.bm=bm
label1.grid()
img_frame.pack()
# root.attributes("-alpha",0.1)
def enter():
    user_list = [('aming','aming'),('csj','csj')]
    if not user_en.get() or not pass_en.get():
        global warning_info
        warning_info.destroy()
        warning_info = Label(img_frame, text='用户名或密码错误', bg='#AFD')
        warning_info.place(x=530, y=240)
        return
    else:
        now_user = ((user_en.get()),(pass_en.get()))
        if now_user in user_list:
            iNt = 9
            while TRUE:
                time.sleep(0.03)
                if iNt == 1:
                    root.destroy()
                    import Manager_body
                    break
                else:
                    ins = '0.'+str(iNt)
                    root.attributes("-alpha", ins)
                    iNt = int(iNt) - 1
        else:
            warning_info.destroy()
            warning_info = Label(img_frame, text='用户名或密码错误', bg='#AFD')
            warning_info.place(x=530, y=240)
def regis():
    global warning_info
    warning_info.destroy()
    warning_info = Label(img_frame, text='暂不提供注册\n请联系QQ:775465751', bg='#AFD')
    warning_info.place(x=530, y=240)
def enter_key(self):
    enter()
Label(img_frame,text='用户名:',bg='#AFD').place(x=335,y=184)
Label(img_frame,text='密   码:',bg='#AFD').place(x=335,y=214)
user_en = ttk.Entry(img_frame)
user_en.bind("<Return>",enter_key)
pass_en = ttk.Entry(img_frame,show='*')
pass_en.bind("<Return>",enter_key)
root.bind("<Return>",enter_key)
warning_info = Label()
bu1 = ttk.Button(img_frame,text='登陆',command=enter)
bu2 = ttk.Button(img_frame,text='注册',command=regis)
bu1.place(x=545,y=182)
bu2.place(x=545,y=212)
user_en.place(x=390,y=184)
pass_en.place(x=390,y=214)
root.mainloop()