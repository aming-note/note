#coding:utf8
from tkinter import *

root= Tk()
w = Canvas(root,width=200,height=200,background="white")
w.pack()
w.create_line(0, 100,200, 100,fill='yellow')
w.create_line(100, 0,100, 200,fill='red',dash = (4, 4))
root.mainloop()