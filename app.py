import ctypes
import tkinter as tk
from datetime import datetime

from ttkbootstrap import ttk

import config
import logger

version = "v2.0.0"


class App:
    width = 600
    height = 500
    log = None
    configs = None
    now = None

    def __init__(self, root):
        # 告诉操作系统使用程序自身的dpi适配
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 获取屏幕的缩放因子
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        # 设置程序缩放
        root.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.width *= (ScaleFactor / 100)
        self.height *= (ScaleFactor / 100)

        configs = self.configs = config.Config()
        configs.init()
        # 助手界面
        root.title("阴阳师助手 %s" % version)
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % \
                    (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        root.geometry(align_str)
        root.resizable(width=False, height=False)
        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # 标签页
        notebook = ttk.Notebook(root)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="助手")
        tab1.config(padding=10)
        self.regTab1(tab1)

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="单开养号")
        tab2.config(padding=10)
        self.regTab2(tab2)

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="组队刷刷")
        tab3.config(padding=10)
        self.regTab3(tab3)

        notebook.grid(row=0, column=0, sticky=tk.NSEW)

    def regTab1(self, tab):
        # 日志
        logFrame = ttk.Frame(tab)
        logFrame.rowconfigure(0, weight=1)
        logFrame.columnconfigure(0, weight=1)
        self.log = tk.Text(logFrame, state="disabled", width=40, height=25)
        self.log.pack()
        logFrame.grid(row=0, column=0, sticky=tk.EW)

        baseConfigs = self.configs.configs["基本设置"]
        tempConfigs = self.configs.configs["临时"]
        baseFrame = ttk.Frame(tab, padding=(5, 0, 0, 0))
        ttk.Label(baseFrame, text="助手模式").grid(row=0, column=0)
        ttk.Combobox(baseFrame, textvariable=baseConfigs["模式"], values=["单开养号", "组队刷刷"],
                     state='readonly').grid(row=0, column=1, padx=5)

        ttk.Label(baseFrame, text="当前时间").grid(row=1, column=0)
        clock = ttk.Label(baseFrame, text="")
        clock.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.clock(tab, clock)

        ttk.Label(baseFrame, text="当前位置").grid(row=2, column=0)
        ttk.Label(baseFrame, textvariable=tempConfigs["当前位置"]).grid(row=2, column=1, sticky=tk.W, padx=5)

        baseFrame.grid(row=0, column=1, sticky=tk.NW)

    def regTab2(self, tab):
        print(1)

    def regTab3(self, tab):
        print(2)

    def clock(self, root, label):
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label.configure(text=self.now)
        root.after(1000, self.clock, root, label)


if __name__ == "__main__":
    # 注册界面
    tkinter = tk.Tk()
    app = App(tkinter)

    # 注册日志监听
    logger.init(app)

    # 启动助手界面
    tkinter.mainloop()
