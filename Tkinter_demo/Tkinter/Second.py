from tkinter import *
from tkinter.simpledialog import *


root = Tk()
def printEvent(event):
    print('<instance>',event.keycode)
# Return 事件处理函数
def printToplevel(event):
    print('<toplevel>',event.keycode)
def printClass(event):
    print('<bind_class>',event.keycode)
def printAppAll(event):
    print('<bind_all>',event.keycode)
# 在 instance 级别与 printEvent 绑定
bt1 = Button(root,text = 'instance event')
bt1.bind('<Return>',printEvent)
# 在 bt1的 Toplevel 级别与 printToplevel 绑定
bt1.winfo_toplevel().bind('<Return>',printToplevel)
# 在 class 级别绑定事件 printClass
root.bind_class('Button','<Return>',printClass)
# 在 application all 级别绑定 printAppAll
bt1.bind_all('<Return>',printAppAll)
# 将焦点定位到 bt1上，回车一下，结果有4个打印输出。
bt1.focus_set()
bt1.grid()
root.mainloop()