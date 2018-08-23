#coding:utf-8
from tkinter import *
root = Tk()
def printEvent(event):
    output.set(event.keycode)
output = StringVar()
out = Entry(root,textvariable=output,)
out['state']='readonly'
out.grid(row=1,column=1)
root.bind('<Key>',printEvent)
root.bind('<Return>',printEvent)
root.mainloop()