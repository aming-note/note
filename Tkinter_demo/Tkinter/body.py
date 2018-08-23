#coding:utf-8
from tkinter import *
from tkinter import ttk
from sour import site_link
import time

window = Tk()
window.title('资源站')
def center_window(tl, width, height):
    screenwidth = tl.winfo_screenwidth()
    screenheight = tl.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    tl.geometry(size)
    return
def war():
    tl = Toplevel(window)
    center_window(tl, 300, 210)
    tl.maxsize(250, 100)
    tl.minsize(250, 100)
    tl.title('信息')
    Label(tl, text='请与开发者联系\nEmail：mingserverwarning@gmail.com', fg='blue', wraplength=500,
          justify='center').pack()
    win.update()
# def daohang_source():
#     p1["value"] = 20
#     window.update()
#     url = "http://www.zhaoavdh.top/"
#     p1["value"] = 40
#     window.update()
#     try:
#         content = requests.get(url,verify=False, timeout=15, allow_redirects=False).content
#         p1["value"] = 60
#         window.update()
#         source = content.decode('gbk')
#         sp1 = re.findall(r'<li>.*</li>',source)
#         p1["value"] = 80
#         window.update()
#         for i in sp1:
#             res1 = re.split(r'href=\"',i)
#             res = re.split(r'"',res1[1])
#             name = re.split(r'[><]',res1[1])
#             date = name[1]+res[0]+'\n'
#             t1.insert(1.0,date)
#         p1["value"] = 100
#         window.update()
#         time.sleep(0.5)
#         p1["value"] = 0
#         window.update()
#     except Exception as e:
#         print(e)
# def tupian_source():
#     p1["value"] = 20
#     window.update()
#     url = "http://www.zhaoavdh.top/"
#     try:
#         content = requests.get(url,verify=False, timeout=15, allow_redirects=False).content
#         p1["value"] = 40
#         window.update()
#         source = content.decode('gbk')
#         sp1 = re.findall(r'<a href=".*',source)
#         p1["value"] = 60
#         window.update()
#         for i in sp1:
#             res1 = re.split(r'<a href="',i)
#             res2 = re.split(r'"',res1[1])
#             res3 = re.findall(r'http://.*',res2[0])
#             name = re.split(r'[><]',res1[1])
#             if not res3:
#                 continue
#             else:
#                 data = name[1]+res3[0]+'\n'
#                 t1.insert(1.0,data)
#         p1["value"] = 100
#         window.update()
#         time.sleep(0.5)
#         p1["value"] = 0
#         window.update()
#     except Exception as e:
#         print(e)


center_window(window, 390, 260)
window.maxsize(390,260)
window.minsize(390,260)

def daohang_source():
    p1["value"]=30
    window.update()
    res = site_link.get_url('')
    kong = []
    for i in res:
        if i in kong:
            continue
        else:
            kong.insert(-1,i)
    for a in kong:
        t1.insert(0.1,a)
    p1["value"]=100
    window.update()
    time.sleep(0.5)
    p1["value"]=0
    window.update()
win = Frame(window)
sc =Scrollbar(win)
t1 = Text(win,width='50',height='10')
sc.pack(side=RIGHT,fill=Y)
t1.pack(side=LEFT,fill=Y)
sc.config(command=t1.yview)
t1.config(yscrollcommand=sc.set)


win1 = Frame(window)
b1 = ttk.Button(win1,text='获取',command=daohang_source)
b1.grid(row=1,column=0)
# b2 = ttk.Button(win1,text='获取图片站',command=tupian_source)
# b2.grid(row=1,column=1)
war = ttk.Button(win1,text='反馈',command=war)
war.grid(row=1,column=2)

win2=Frame(window)
p1 = ttk.Progressbar(win2,length=380,mode="determinate",orient=HORIZONTAL)
p1.grid(row=0,column=0)
p1["maximum"] = 100
p1["value"] = 0

win3 = Frame(window)
Label(win3,text='个别资源需要翻墙才可浏览,如有其他问题,那就有吧,反正也解决不了！！').pack()

win.grid(row=0,column=0,padx=8, pady=8, ipadx=4)
win1.grid(row=3,column=0,padx=8, pady=8, ipadx=4)
win2.grid(row=1,column=0,padx=1, pady=8, ipadx=8)
win3.grid(row=2,column=0)
window.mainloop()