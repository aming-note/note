#coding:gb2312
from tkinter import *
from tkinter import ttk
import requests,re,time
#��������Ƿ�Ϸ��ĺ���
def check():
    if v.get() == '':
        s.set('������Ϸ���IP��ַ')
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
def center_window(tl, width, height):
        screenwidth = tl.winfo_screenwidth()
        screenheight = tl.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        tl.geometry(size)
        return

def info(): #��ȡIP�Ĺ����ز���ʵ���½�����
    p1["value"] = 20    #���ڸ��½��������ȣ�p1["value"]Ϊ�������Ľ���ֵ
    win.update()        #����win���
    url = "https://www.ip.cn/index.php?ip=" + v.get()
    try:#�����Ƿ���Դ�������URL
        requests.packages.urllib3.disable_warnings()
        requests.get(url, verify=False, timeout=3, allow_redirects=False).content
    except Exception as e:#�򲻿��򵯱�����
        tl = Toplevel(window)
        center_window(tl, 300, 210)
        tl.maxsize(250,100)
        tl.minsize(250,100)
        tl.title('����')
        Err = StringVar()
        Label(tl,text='�������쳣\n���������������ӻ���ϵ�������޸�\nEmail��mingserverwarning@gmail.com',fg='red',wraplength=500,justify='center').pack()
        Err.set(e)
        p1["value"] = 0  # ���ý�����
        win.update()
        return
    else:#�������������ִ�����´���
        requests.packages.urllib3.disable_warnings()
        p1["value"] = 40
        win.update()
        content = requests.get(url, verify=False, timeout=5, allow_redirects=False).content
        p1["value"] = 60
        win.update()
        source = content.decode('utf-8')    #��ȡ��ҳԴ�벢��תΪ���ģ����¶���Re��ȡ����
        res_line = re.findall(r'<div id="result"><div class="well"><p>����ѯ�� IP��<code>(.*)</p></div></div>', source)
        res = re.split(r'<p>', res_line[0])
        pos_exc = re.split(r'���ڵ���λ�ã�<code>', res[1])
        p1["value"] = 80
        win.update()
        pos = re.split(r'</code></p>', pos_exc[1])
        p1["value"] = 100
        win.update()
        s.set(pos[0])   #����s���ֵ������Entry��ʾ
        time.sleep(0.5)
        p1["value"] = 0 #���ý�����
        win.update()
        return
# def clear_def(event): #���������е�Ĭ����ʾ���֣���BUG
#     v.set('')
window = Tk()
window.title('IP�����ز�ѯ')
window.configure(background='#FFC')
window.iconbitmap('c:\\sun.ico')

#���º���Ϊ���ô����λ������Ļ����
def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(size)
    return
center_window(window, 300, 240)
window.maxsize(250,130)
window.minsize(250,130)
#����Ϊ�����ڲ�����������
win = Frame(window,bg='#FFC')   #����Frame����������Ű�

#����Ϊ��������Ϣ
p1 = ttk.Progressbar(win,length=140,mode="determinate",orient=HORIZONTAL)   #����������
p1.grid(row=2,column=2) #������λ��
p1["maximum"] = 100 #���������ֵ
p1["value"] = 0 #������Ĭ��λ��

#����Ϊ��ע
rem = Label(win,text='By aminG',bg='#FFC')  #��ע��Ϣ
rem.grid(row=3,column=0)

#����Ϊ�����飬�����������ڷ�����ºͻ�ȡEntry����Ϣ
v = StringVar() #������
s = StringVar() #�����

#����Ϊ����Ԫ�أ�����Label��Entry��Button
lab1 = Label(win, text="����IP:",bg='#FFC')
lab1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

en = Entry(win,textvariable=v)  #�����
#��������Ϊ����ı�������ı����е����ݣ�Ŀ��Ϊ��Ĭ����ʾ���֣�����BUG��ÿ�ε���������
# en.bind("<ButtonPress>",clear_def)
# v.set('���ٴ�����IP��ַ')
en.grid(row=0, column=1, sticky='ew', columnspan=2)

lab2 = Label(win, text="������:",bg='#FFC')
lab2.grid(row=1, column=0, padx=5, pady=5, sticky=W)

en2 = Entry(win,textvariable=s,state='readonly') #�����
en2.grid(row=1, column=1, sticky='ew', columnspan=2)

bu = ttk.Button(win,text='��ѯ',command=check)   #��ѯ��ť
bu.grid(row=2, column=0)

win.pack(padx=8, pady=8, ipadx=4)   #Frame��λ������
window.mainloop()
