#coding:utf8
from tkinter import *
from tkinter import ttk

win = Tk()
win.geometry('300x300')
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='第一页')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='第二页')
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='第三页')
tabControl.pack(expand=1, fill="both")
win.mainloop()