from tkinter import *
from tkinter import ttk
class app():
    def __init__(self):
        self.root = Tk()
        self.root.title("痒痒鼠命中概率计算器")
        self.root.geometry('%dx%d+%d+%d' % (300, 500, (self.root.winfo_screenwidth() - 300) / 2, (self.root.winfo_screenheight() - 700) / 2))
        self.body()
        self.root.mainloop()
    def body(self):
        num_1 = IntVar()
        num_2 = IntVar()
        num_3 = IntVar()
        count = ttk.Entry(self.root,width="20",textvariable=num_1)
        default = ttk.Entry(self.root,width="20",textvariable=num_2)
        addition = ttk.Entry(self.root,width="20",textvariable=num_3)
        Label(self.root, text="攻击次数: ").place(x=30, y=110)
        count.place(x=100,y=110)
        Label(self.root, text="基础命中: ").place(x=30, y=150)
        default.place(x=100,y=150)
        Label(self.root, text="命中加成: ").place(x=30, y=190)
        addition.place(x=100,y=190)
        text = Text(self.root,width=42,height=15)
        text.place(x=0,y=300)
        def click():
            res = int(num_2.get()) * int(num_3.get()) + int(num_2.get())
            return res
app()