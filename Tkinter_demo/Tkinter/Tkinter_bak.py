#coding:gb2312
from tkinter import *
from tkinter import ttk
import requests,re,time
#检查输入是否合法的函数
def check():
    if v.get() == '':
        s.set('请输入合法的IP地址')
        return
    else:
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, v.get()):
            info()
            return
        else:
            s.set('请输入合法的IP地址')
            v.set('')
            return
def center_window(tl, width, height):
        screenwidth = tl.winfo_screenwidth()
        screenheight = tl.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        tl.geometry(size)
        return

def info(): #获取IP的归属地并事实更新进度条
    p1["value"] = 20    #用于更新进度条进度，p1["value"]为进度条的进度值
    win.update()        #更新win组件
    url = "https://www.ip.cn/index.php?ip=" + v.get()
    try:#测试是否可以打开以以上URL
        requests.packages.urllib3.disable_warnings()
        requests.get(url, verify=False, timeout=3, allow_redirects=False).content
    except Exception as e:#打不开则弹报错窗口
        tl = Toplevel(window)
        center_window(tl, 300, 210)
        tl.maxsize(250,100)
        tl.minsize(250,100)
        tl.title('错误')
        Err = StringVar()
        Label(tl,text='程序处理异常\n请检查您的网络链接或联系开发者修复\nEmail：mingserverwarning@gmail.com',fg='red',wraplength=500,justify='center').pack()
        Err.set(e)
        p1["value"] = 0  # 重置进度条
        win.update()
        return
    else:#如果测试正常则执行以下代码
        requests.packages.urllib3.disable_warnings()
        p1["value"] = 40
        win.update()
        content = requests.get(url, verify=False, timeout=5, allow_redirects=False).content
        p1["value"] = 60
        win.update()
        source = content.decode('utf-8')    #获取网页源码并且转为中文，以下都是Re截取操作
        res_line = re.findall(r'<div id="result"><div class="well"><p>您查询的 IP：<code>(.*)</p></div></div>', source)
        res = re.split(r'<p>', res_line[0])
        pos_exc = re.split(r'所在地理位置：<code>', res[1])
        p1["value"] = 80
        win.update()
        pos = re.split(r'</code></p>', pos_exc[1])
        p1["value"] = 100
        win.update()
        s.set(pos[0])   #设置s组的值，用于Entry显示
        time.sleep(0.5)
        p1["value"] = 0 #重置进度条
        win.update()
        return
# def clear_def(event): #情况输入框中的默认提示文字，有BUG
#     v.set('')
window = Tk()
window.title('IP归属地查询')
window.configure(background='#FFC')
window.iconbitmap('c:\\sun.ico')

#以下函数为设置窗体打开位置于屏幕居中
def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(size)
    return
center_window(window, 300, 240)
window.maxsize(250,130)
window.minsize(250,130)
#以上为主窗口参数，不解释
win = Frame(window,bg='#FFC')   #创建Frame插件，便于排版

#以下为进度条信息
p1 = ttk.Progressbar(win,length=140,mode="determinate",orient=HORIZONTAL)   #创建进度条
p1.grid(row=2,column=2) #进度条位置
p1["maximum"] = 100 #进度条最大值
p1["value"] = 0 #进度条默认位置

#以下为备注
rem = Label(win,text='By aminG',bg='#FFC')  #备注信息
rem.grid(row=3,column=0)

#以下为两个组，这两个组用于方便更新和获取Entry的信息
v = StringVar() #输入组
s = StringVar() #输出组

#以下为所有元素，包括Label和Entry，Button
lab1 = Label(win, text="输入IP:",bg='#FFC')
lab1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

en = Entry(win,textvariable=v)  #输入框
#以下两行为点击文本框情况文本框中的内容，目的为有默认提示文字，但有BUG，每次点击都会清空
# en.bind("<ButtonPress>",clear_def)
# v.set('请再次输入IP地址')
en.grid(row=0, column=1, sticky='ew', columnspan=2)

lab2 = Label(win, text="归属地:",bg='#FFC')
lab2.grid(row=1, column=0, padx=5, pady=5, sticky=W)

en2 = Entry(win,textvariable=s,state='readonly') #输出框
en2.grid(row=1, column=1, sticky='ew', columnspan=2)

bu = ttk.Button(win,text='查询',command=check)   #查询按钮
bu.grid(row=2, column=0)

win.pack(padx=8, pady=8, ipadx=4)   #Frame的位置属性
window.mainloop()
