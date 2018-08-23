#coding:utf8
import socket,threading,time,datetime,os
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from openpyxl import Workbook
from tkinter import messagebox as mBox

root = Tk()
root.geometry('%dx%d+%d+%d' % (700, 500, (root.winfo_screenwidth() - 700) / 2, (root.winfo_screenheight() - 700) / 2))
root.title('Servers Manage')
root.maxsize(700,500)
root.minsize(700,500)
pwd = os.getcwd()
logo = PhotoImage(file=pwd+'\\logo.gif')
root.tk.call('wm','iconphoto',root._w,logo)
img_frame=Frame(root,height=100,width=100)
save_excel_data = []
def check_server_status():
    start = time.clock()
    text.delete(0.0,END)
    text.insert(END,'--------------------------------------------------\n')
    text.insert(END,'开始检查服务器,请确保所有服务器均已运行服务端程序\n')
    text.insert(END, '--------------------------------------------------\n')
    info_fra.update()
    err_host = []
    for i in addr_list:
        def Many_Thread(i,a):
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(5)
            try:
                conn.connect(i)
                info = '--> 服务器响应正常'+str(i[0])+':'+str(a)+'\n'
                conn.close()
                text.insert(END,info)
                info_fra.update()
            except:
                info = '--> 服务器响应异常'+str(i[0])+':'+str(a)+'\n'
                text.insert(END, info)
                info_fra.update()
        t = threading.Thread(target=Many_Thread,args=(i[0],i[1]))
        t.start()
    # if not err_host:
    #     text.insert(END, '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    #     text.insert(END, '没有异常主机\n')
    #     info_fra.update()
    # else:
    #     text.insert(END, '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    #     text.insert(END, '以下主机无法连接:\n')
    #     for a in err_host:
    #         res_info = str(a)+'\n'
    #         text.insert(END,res_info)
    #         info_fra.update()
def get_resource():
    save_excel_data.clear()
    text.delete(0.0, END)
    text.insert(END, '--------------------------------------------------\n')
    text.insert(END, '--> 正在获取所有服务器资源,比较慢,请勿轻举妄动\n')
    text.insert(END, '--------------------------------------------------\n')
    text.update()
    item = T1.get_children()
    def for_get():
        for i in item:
            T1.delete(i)
        command = ['get_os_type','get_os_info', 'get_cpu_count', 'get_cpu_version', 'get_mem_total', 'get_mem_used','get_mem_free']
        get_all_value = []
        num = 0
        for addr in addr_list:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                conn.connect(addr[0])
                info = '--> 正在获取服务器资源' + str(addr[0][0]) + ':' + str(addr[1]) + '\n'
                text.insert(END, info)
                conn_info = conn.recv(1024)
                # text.insert(END, ('--> '+str(conn_info.decode())+'\n'))
                # text.insert(END, '--------------------------------------------------\n')
                for com in command:
                    conn.send(com.encode())
                    getvalue = conn.recv(1024)
                    get_all_value.insert(-1,getvalue.decode())
                num = num + 1
                T1.insert("", num, text=num, values=(num,addr[0][0],addr[1],get_all_value[6],get_all_value[0],get_all_value[1],get_all_value[2],get_all_value[3],get_all_value[4],get_all_value[5]))
                save_excel_data.insert(0,(num,addr[0][0],addr[1],get_all_value[6],get_all_value[0],get_all_value[1],get_all_value[2],get_all_value[3],get_all_value[4],get_all_value[5]))
                info_fra.update()
                get_all_value.clear()
                conn.close()
                continue
            except:
                errinfo = '--> 无法获取服务器资源' + str(addr[0][0]) + ':' + str(addr[1]) + '\n'
                info_fra.update()
                text.insert(END,errinfo)
                continue
        text.insert(END, '--> 本次资源已获取完毕\n')
    for_get_threa = threading.Thread(target=for_get)
    for_get_threa.start()
def save_as_excel():
    if not T1.get_children():
        text.insert(END,'--> 请先获取资源列表\n')
    else:
        if os.path.isdir(os.getcwd() + '\\note') == TRUE:
            i = datetime.datetime.now()
            today = str(i.year) + '-' + str(i.month) + '-' + str(i.day)
            try:
                wb = Workbook()
                sheet = wb.active
                sheet.title='sheet1'
                title_info = ('序号','主机地址','备注信息','系统类型','系统版本','CPU数量','CPU版本','内存总量','已用内存','剩余内存')
                sheet.append(title_info)
                for i in save_excel_data:
                    sheet.append(i)
                filename = os.getcwd() + '\\note\\' + today + '.xlsx'
                wb.save(filename=filename)
                text.insert(END,'--> 成功保存文件:' + filename)
            except Exception as e:
                print(e)
                text.insert(END, '--> 未能成功保存文档')
        else:
            text.insert(END, '--> 首次运行程序，正在创建数据目录...\n')
            os.mkdir(os.getcwd() + '\\note')
            save_as_excel()
def add_host_operation():
    if not en2.get() or '\x00' in en2.get():
        text.insert(0.0, '--> 请输入合法IP地址和端口\n')
    else:
        des_ip = en1.get()
        des_port = en2.get()
        add_host = (str(des_ip), int(des_port))
        try:
            res = socket.getaddrinfo(des_ip, 0, socket.AF_UNSPEC,
                                     socket.SOCK_STREAM,
                                     0, socket.AI_NUMERICHOST)
            if add_host in addr_list:
                text.insert(0.0,'--> 此主机已存在\n')
            else:
                if not des_port:
                    text.insert(0.0,'--> 请输入端口号\n')
                elif int(des_port) > 1 and int(des_port) < 65535:
                    addr_list.insert(-1,add_host)
                    text.insert(0.0,'--> 添加成功\n')
                else:
                    text.insert(0.0,'--> 请输入合法IP地址和端口\n')
        except:
            text.insert(0.0,'--> 请输入合法IP和端口\n')
def del_host_operation():
    if not en2.get() or '\x00' in en2.get():
        text.insert(0.0, '--> 请输入合法IP地址和端口\n')
    else:
        des_ip = en1.get()
        des_port = en2.get()
        dest_host = (str(des_ip), int(des_port))
        try:
            res = socket.getaddrinfo(des_ip, 0, socket.AF_UNSPEC,
                                     socket.SOCK_STREAM,
                                     0, socket.AI_NUMERICHOST)
            if dest_host in addr_list:
                addr_list.pop(addr_list.index(dest_host))
                text.insert(0.0,'--> 删除成功\n')
            else:
                text.insert(0.0,'--> 此主机不在列表中\n')
        except:
            text.insert(0.0,'--> 请输入合法IP地址和端口\n')
def search_operation():
    if not T1.get_children():
        text.insert(END,'--> 请先获取资源列表后再执行查询操作\n')
    else:
        if not en1.get() and not en2.get():
            text.insert(END, '--> 请输入查询条件\n')
            text.update()
        else:
            find_host = []
            T1.selection_set('')
            des_ip = en1.get()
            if not en1.get():
                all_value = T1.get_children()
                for i in all_value:
                    res = T1.item(i)['values']
                    if en2.get() == res[2]:
                        T1.selection_set(i)
                        find_host.insert(0, i)
                        text.insert(END, '--> 已找到,已将指定主机高亮显示\n')
                        continue
                if not find_host:
                    text.insert(END, '--> 没找到指定主机,请检查输入条件1\n')
            else:
                try:
                    res = socket.getaddrinfo(des_ip, 0, socket.AF_UNSPEC,
                                             socket.SOCK_STREAM,
                                             0, socket.AI_NUMERICHOST)
                    all_value = T1.get_children()
                    for i in all_value:
                        res = T1.item(i)['values']
                        if en1.get() == res[1]:
                            T1.selection_set(i)
                            find_host.insert(0,i)
                            text.insert(END,'--> 已找到,已将指定主机高亮显示\n')
                            continue
                    if not find_host:
                        text.insert(END, '--> 没找到指定主机,请检查输入条件2\n')
                except:
                    text.insert(END,'--> 请输入合法的IP地址\n')
def search_key(self):
    search_operation()
def operation_command():
    text.delete(0.0, END)
    text.insert(END, '--------------------------------------------------\n')
    text.insert(END, '开始向所有服务器发送该指令\n')
    text.insert(END, '--------------------------------------------------\n')
    info_fra.update()
    for i in addr_list:
        def Many_Thread(i, a):
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(5)
            try:
                conn.connect(i)
                verfy_info = conn.recv(1024)
                # text.insert(END, '--> ' + verfy_info.decode() + '\n')
                conn.send((com_en.get()).encode())
                recv_data = conn.recv(1024)
                text.insert(END,'--> ' + str(i[0]) + ':' + str(recv_data.decode()) + '\n')
                conn.close()
                info_fra.update()
            except:
                info = '--> 服务器响应异常' + str(i[0]) + ':' + str(a) + '\n'
                text.insert(END, info)
                info_fra.update()

        t = threading.Thread(target=Many_Thread, args=(i[0], i[1]))
        t.start()
def flush():
    text.delete(0.0,END)
    for i in T1.get_children():
        T1.delete(i)
    en1.delete(0,END)
    en2.delete(0,END)
    root.update()
def dump_info():
    mBox.showinfo('错误', '通知:XXXXXX')
root_fra = Frame(root,width=700,height=500,bg='#F5B9EF')
button_fra = Frame(root_fra,width=305,height=140,bg='#ACAFE2')
info_fra = Frame(root_fra,width=380,height=235,bg='#CBF')
resource_fra = Frame(root_fra,width=280,height=310)
search_fra = Frame(root_fra,width=305,height=87,bg='#88B460')
# add_host_fra = Frame(root,width=230,height=70)
text = Text(info_fra,width=50,height=18,bg='#A6A7B9')
# text.configure(state='disabled')
text["foreground"] = 'black'
addr_list = [(('45.77.37.190',6666),'反馈'),
             (('23.27.167.88',6666),'竞技榜'),
             (('182.255.63.176',6666),'活动'),
             (('118.24.148.24',6666),'APP下载'),
             (('45.125.49.9',6666),'FH充值'),
             (('23.27.167.210',6666),'FH快充'),
             (('43.229.154.32', 6666), '500快充'),
             (('103.40.112.97', 6666), '落地页'),]
Label(resource_fra,text='资源信息').grid()
T1 = ttk.Treeview(resource_fra, height=10, show="headings")
T1["column"] = ('ID','主机地址','备注信息', '系统类型','系统版本', 'CPU数量', 'CPU版本','内存总量','已用内存','剩余内存')
T1.column('ID', width='25')
T1.column('主机地址', width='80')
T1.column('备注信息', width='70')
T1.column('系统类型', width='80')
T1.column('系统版本', width='80')
T1.column('CPU数量', width='60')
T1.column('CPU版本', width='60')
T1.column('内存总量', width='65')
T1.column('已用内存', width='65')
T1.column('剩余内存', width='65')
T1.heading('ID', text='ID')
T1.heading('主机地址', text='主机地址')
T1.heading('备注信息', text='备注信息')
T1.heading('系统类型', text='系统类型')
T1.heading('系统版本', text='系统版本')
T1.heading('CPU数量', text='CPU数量')
T1.heading('CPU版本', text='CPU版本')
T1.heading('内存总量', text='内存总量')
T1.heading('已用内存', text='已用内存')
T1.heading('剩余内存', text='剩余内存')
Bar = ttk.Scrollbar(resource_fra, orient=VERTICAL, command=T1.yview)
T1.configure(yscrollcommand=Bar.set)

but1 = ttk.Button(button_fra,text='列出所有',command=check_server_status)
but2 = ttk.Button(button_fra,text='导出Excel',command=save_as_excel)
but4 = ttk.Button(button_fra,text='资源获取',command=get_resource)
but5 = ttk.Button(button_fra,text='添加/删除',command=dump_info)
com_en = ttk.Entry(button_fra)
but6 = ttk.Button(button_fra,text='执行命令',command=operation_command)
but6.place(x=165,y=100)
com_en.place(x=12,y=103)
but1.place(x=45,y=10)
but2.place(x=45,y=55)
but4.place(x=165, y=10)
but5.place(x=165, y=55)
# Label(add_host_fra,text='添加/删除主机').grid(row=0,column=1)
# Label(add_host_fra,text='IP:').grid(row=1,column=0)
# en1 = ttk.Entry(add_host_fra)
# en1.grid(row=1,column=1)
# Label(add_host_fra,text='端口:').grid(row=2,column=0)
# en2 = ttk.Entry(add_host_fra)
# en2.grid(row=2,column=1)
# add_but = ttk.Button(add_host_fra,text='添加',command=add_host_operation)
# add_but.grid(row=1,column=2)
# del_but = ttk.Button(add_host_fra,text='删除',command=del_host_operation)
# del_but.grid(row=2,column=2)
ft = tkFont.Font(family = 'Arial',size = 13,weight = tkFont.BOLD)
Label(search_fra,text='查询',bg='#88B460',font=ft).place(x=115,y=0)
Label(search_fra,text='按  IP',bg='#88B460').place(x=0,y=25)
Label(search_fra,text='按备注',bg='#88B460').place(x=0,y=55)
en1 = ttk.Entry(search_fra)
en2 = ttk.Entry(search_fra)
en1.place(x=50,y=25)
en1.bind("<Return>",search_key)
en2.place(x=50,y=55)
en2.bind("<Return>",search_key)
B1 = ttk.Button(search_fra,text='查找',command=search_operation)
B2 = ttk.Button(search_fra,text='清屏',command=flush)
B1.place(x=205,y=23)
B2.place(x=205,y=53)
Bar.grid(row=0, column=1, sticky=NS)
T1.grid(row=0, column=0)
text.grid()

button_fra.place(x=380,y=347)
info_fra.place(x=15,y=250)
search_fra.place(x=380,y=250)
# add_host_fra.place(x=425,y=240)
resource_fra.place(x=15,y=10)
root_fra.pack()
root.mainloop()