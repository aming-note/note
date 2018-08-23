#coding:gb2312
from tkinter import *
import requests,re,time
from tkinter import ttk

def check():
    if v.get() == '':
        s.set('������Ϸ���IP��ַ')
        return
    elif v.get() == 'i':
        Myip()
        return
    else:
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, v.get()):
            info()
            return
        else:
            s.set('������Ϸ���IP��ַ')
            v.set('')
            return
def check_2(self):
    check()
def center_window(tl, width, height):
        screenwidth = tl.winfo_screenwidth()
        screenheight = tl.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        tl.geometry(size)
        return
def Myip():
    s.set('Loding...')
    p1["value"] = 20
    win.update()
    url = "http://myip.ipip.net/"
    try:
        p1["value"] = 30
        win.update()
        content = requests.get(url, verify=False, timeout=15, allow_redirects=False).content
        source = content.decode('utf8')
        p1["value"] = 50
        win.update()
        wepos = re.split(r'  �����ڣ�', source)
        p1["value"] = 80
        win.update()
        weip = re.split(r'��ǰ IP��', wepos[0])
        pos = wepos[1]
        p1["value"] = 90
        win.update()
        iip = weip[1]
        s.set(pos)
        v.set('����IP:' + iip)
        p1["value"] = 100
        win.update()
        time.sleep(0.3)
        p1["value"] = 0
        win.update()
        return
    except Exception as e:
        tl = Toplevel(window)
        center_window(tl, 300, 210)
        tl.maxsize(250, 100)
        tl.minsize(250, 100)
        tl.title('����')
        tl.iconbitmap('c:\\sun.ico')
        Err = StringVar()
        Label(tl, text='���ӳ�ʱ\n���������������ӻ���ϵ�������޸�\nEmail��mingserverwarning@gmail.com',fg='red',wraplength=500,justify='center').pack()
        Err.set(e)
        p1["value"] = 0
        win.update()
        return
def WriteHosts():
    addr_list = [
        '192.168.0.202 google.com',
        '192.168.0.202 www.google.com',
    ]
    file = open('C:\\windows\\System32\\drivers\\etc\\hosts','a+')
    for i in addr_list:
        file.write(i +'\n')
    file.close()
def info():
    s.set('Loding...')
    p1["value"] = 20
    win.update()
    url = "https://www.ip.cn/index.php?ip=" +v.get()
    try:
        requests.packages.urllib3.disable_warnings()
        p1["value"] = 30
        win.update()
        content = requests.get(url, verify=False, timeout=15, allow_redirects=False).content
        p1["value"] = 50
        win.update()
        source = content.decode('utf-8')
        res_line = re.findall(r'<div id="result"><div class="well"><p>����ѯ�� IP��<code>(.*)</p></div></div>', source)
        res = re.split(r'<p>', res_line[0])
        pos_exc = re.split(r'���ڵ���λ�ã�<code>', res[1])
        p1["value"] = 80
        win.update()
        pos = re.split(r'</code></p>', pos_exc[1])
        p1["value"] = 100
        win.update()
        local_net = re.split(r'</code>', pos[0])
        s.set(local_net[0])
        time.sleep(0.5)
        p1["value"] = 0
        win.update()
        return
    except Exception as e:
        tl = Toplevel(window)
        center_window(tl, 300, 210)
        tl.maxsize(250,100)
        tl.minsize(250,100)
        tl.title('����')
        tl.iconbitmap('c:\\sun.ico')
        Err = StringVar()
        Label(tl,text='���ӳ�ʱ\n���������������ӻ���ϵ�������޸�\nEmail��mingserverwarning@gmail.com',fg='red',wraplength=500,justify='center').pack()
        Err.set(e)
        p1["value"] = 0
        win.update()
        return
window = Tk()
window.title('IP�����ز�ѯ')
window.configure(background='#FFC')
center_window(window, 300, 240)
window.maxsize(250,130)
window.minsize(250,130)
#����Ϊ�����ڲ�����������
win = Frame(window,bg='#FFC')
#����Ϊ��������Ϣ
p1 = ttk.Progressbar(win,length=140,mode="determinate",orient=HORIZONTAL)
p1.grid(row=2,column=2)
p1["maximum"] = 100
p1["value"] = 0
#����Ϊ��ע
rem = Label(win,text='By aminG',bg='#FFC')
rem.grid(row=3,column=0)
rem2 = Label(win,text='������ĸ i �鿴����IP',bg='#FFC')
rem2.grid(row=3,column=2)
v = StringVar() #������
s = StringVar() #�����
lab1 = Label(win, text="����IP:",bg='#FFC')
lab1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
en = Entry(win,textvariable=v)  #�����
en.bind('<Return>',check_2)
en.grid(row=0, column=1, sticky='ew', columnspan=2)
lab2 = Label(win, text="������:",bg='#FFC')
lab2.grid(row=1, column=0, padx=5, pady=5, sticky=W)
en2 = Entry(win,textvariable=s,state='readonly') #�����
en2.grid(row=1, column=1, sticky='ew', columnspan=2)
bu = ttk.Button(win,text='��ѯ',command=check)   #��ѯ��ť
bu.grid(row=2, column=0)
win.pack(padx=8, pady=8, ipadx=4)
window.mainloop()
# WriteHosts()  #��Hosts�ļ�