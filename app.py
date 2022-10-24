import ctypes
import os
from ctypes import wintypes
import tkinter as tk
from datetime import datetime
from threading import Thread
from tkinter import messagebox

import win32con
from ttkbootstrap import ttk

import config
import logger
import script

version = "v2.4.0"
user32 = ctypes.windll.user32  # 加载user32.dll
path = os.getcwd()
imgPath = path + "\\img\\"
tempImgPath = imgPath + "temp\\"


class App:
    width = 600
    height = 550
    log = None  # 日志框
    configs = None  # 配置表
    now = None  # 当前时间

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

        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="活动模式")
        tab4.config(padding=10)
        self.regTab4(tab4)

        tipsTab = ttk.Frame(notebook)
        notebook.add(tipsTab, text="使用说明")
        self.regTipsTab(tipsTab)

        updateTab = ttk.Frame(notebook)
        notebook.add(updateTab, text="更新日志")
        self.regUpdateTab(updateTab)

        notebook.grid(row=0, column=0, sticky=tk.NSEW)

    def regTab1(self, tab):
        baseConfigs = self.configs.configs["基本设置"]

        # 日志
        logFrame = ttk.Frame(tab)
        logFrame.rowconfigure(0, weight=1)
        logFrame.columnconfigure(0, weight=1)
        logFrame.grid(row=0, column=0, sticky=tk.EW)

        self.log = tk.Text(logFrame, state="disabled", width=40, height=25)
        self.log.pack()

        baseFrame = ttk.Frame(tab, padding=(5, 0, 0, 0))
        baseFrame.grid(row=0, column=1, sticky=tk.NW)

        ttk.Label(baseFrame, text="按 F10 运行/暂停任务, F11 终止任务") \
            .grid(row=0, column=0, columnspan=99, sticky=tk.W)

        ttk.Label(baseFrame, text="运行状态") \
            .grid(row=1, column=0, pady=3)
        running = ttk.Label(baseFrame, text="", foreground="white")
        running \
            .grid(row=1, column=1, sticky=tk.W, padx=5, pady=3)
        self.running(tab, running)

        ttk.Label(baseFrame, text="助手模式") \
            .grid(row=2, column=0, pady=3)
        ttk.Radiobutton(baseFrame, text="单开养号", value="单开养号", variable=baseConfigs["模式"]) \
            .grid(row=2, column=1, padx=5, sticky=tk.W, pady=3)
        ttk.Radiobutton(baseFrame, text="组队刷刷", value="组队刷刷", variable=baseConfigs["模式"]) \
            .grid(row=2, column=2, padx=5, sticky=tk.W, pady=3)
        ttk.Radiobutton(baseFrame, text="活动模式", value="活动模式", variable=baseConfigs["模式"]) \
            .grid(row=2, column=3, padx=5, sticky=tk.W, pady=3)

        ttk.Label(baseFrame, text="悬赏邀请") \
            .grid(row=3, column=0, pady=3)
        ttk.Radiobutton(baseFrame, text="取消", value="取消", variable=baseConfigs["悬赏邀请"]) \
            .grid(row=3, column=1, padx=5, sticky=tk.W, pady=3)
        ttk.Radiobutton(baseFrame, text="接受", value="接受", variable=baseConfigs["悬赏邀请"]) \
            .grid(row=3, column=2, padx=5, sticky=tk.W, pady=3)
        ttk.Radiobutton(baseFrame, text="拒绝", value="拒绝", variable=baseConfigs["悬赏邀请"]) \
            .grid(row=3, column=3, padx=5, sticky=tk.W, pady=3)

        ttk.Label(baseFrame, text="当前时间") \
            .grid(row=4, column=0, pady=3)
        clock = ttk.Label(baseFrame, text="")
        clock \
            .grid(row=4, column=1, sticky=tk.W, padx=5, columnspan=2, pady=3)
        self.clock(tab, clock)

        ttk.Label(baseFrame, text="当前位置") \
            .grid(row=5, column=0, pady=3)
        local = ttk.Label(baseFrame, text="")
        local.grid(row=5, column=1, sticky=tk.W, padx=5, pady=3)
        self.getScriptStatus(tab, local, "local")

        ttk.Label(baseFrame, text="寮突目标") \
            .grid(row=6, column=0, pady=3)
        local = ttk.Label(baseFrame, text="")
        local.grid(row=6, column=1, sticky=tk.W, padx=5, pady=3)
        self.getScriptStatus(tab, local, "寮突破今日目标")

        ttk.Label(baseFrame, text="剩余次数") \
            .grid(row=7, column=0, pady=3)
        times = ttk.Label(baseFrame, text="")
        times.grid(row=7, column=1, sticky=tk.W, padx=5, pady=3)
        self.getScriptStatus(tab, times, "times")

        ttk.Label(baseFrame, text="延时") \
            .grid(row=8, column=0, pady=3)
        delay = ttk.Label(baseFrame, text="")
        delay.grid(row=8, column=1, sticky=tk.W, padx=5, pady=3)
        self.getScriptStatus(tab, delay, "delay")

        ttk.Button(baseFrame, text="保存配置", command=config.Config().save) \
            .grid(row=9, column=0, columnspan=99, pady=3)

    def regTab2(self, tab):
        dkConfigs = self.configs.configs["单开养号"]
        row1 = tk.Frame(tab)
        base = ttk.LabelFrame(row1, text="基本设置", padding=10)
        ttk.Checkbutton(base, text="任务循环", offvalue=0, onvalue=1, variable=dkConfigs["任务循环"]) \
            .grid(row=0, column=0, padx=5)
        ttk.Label(base, text="休息时间 (分)").grid(row=0, column=1, padx=5)
        ttk.Entry(base, textvariable=dkConfigs["休息时间min"]).grid(row=0, column=2, padx=5)
        ttk.Label(base, text="-", anchor="center").grid(row=0, column=3, padx=5)
        ttk.Entry(base, textvariable=dkConfigs["休息时间max"]).grid(row=0, column=4, padx=5)
        base.grid(row=0, column=0, sticky=tk.W, pady=2)
        row1.grid(row=0, column=0, sticky=tk.W, pady=2)

        row2 = tk.Frame(tab)
        tyjc = ttk.LabelFrame(row2, text="庭院检测", padding=10)
        ttk.Checkbutton(tyjc, text="庭院御魂", offvalue=0, onvalue=1, variable=dkConfigs["庭院御魂"]) \
            .grid(row=0, column=0, padx=5)
        ttk.Checkbutton(tyjc, text="庭院寿司", offvalue=0, onvalue=1, variable=dkConfigs["庭院寿司"]) \
            .grid(row=0, column=1, padx=5)
        ttk.Checkbutton(tyjc, text="庭院勾玉", offvalue=0, onvalue=1, variable=dkConfigs["庭院勾玉"]) \
            .grid(row=0, column=2, padx=5)
        tyjc.grid(row=0, column=0, sticky=tk.W, pady=2)
        row2.grid(row=1, column=0, sticky=tk.W, pady=2)

        row3 = tk.Frame(tab)
        mryc = ttk.LabelFrame(row3, text="每日一次", padding=10)
        ttk.Checkbutton(mryc, text="每日签到", offvalue=0, onvalue=1, variable=dkConfigs["每日签到"]) \
            .grid(row=0, column=0, padx=5)
        ttk.Checkbutton(mryc, text="黄金签到", offvalue=0, onvalue=1, variable=dkConfigs["黄金签到"]) \
            .grid(row=0, column=1, padx=5)
        ttk.Checkbutton(mryc, text="领取黑蛋", offvalue=0, onvalue=1, variable=dkConfigs["领取黑蛋"]) \
            .grid(row=0, column=2, padx=5)
        ttk.Checkbutton(mryc, text="友情点", offvalue=0, onvalue=1, variable=dkConfigs["友情点"]) \
            .grid(row=0, column=3, padx=5)
        ttk.Checkbutton(mryc, text="领取寮资金", offvalue=0, onvalue=1, variable=dkConfigs["领取寮资金"]) \
            .grid(row=0, column=4, padx=5)
        mryc.grid(row=0, column=0, sticky=tk.W, pady=2)
        row3.grid(row=2, column=0, sticky=tk.W, pady=2)

        row4 = tk.Frame(tab)
        jj = ttk.LabelFrame(row4, text="阴阳寮结界", padding=10)
        ttk.Checkbutton(jj, text="开启", offvalue=0, onvalue=1, variable=dkConfigs["阴阳寮结界"]) \
            .grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(jj, text="间隔 (时)", anchor="e").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(jj, textvariable=dkConfigs["阴阳寮结界间隔"], values=["1", "2", "3", "4", "5", "6"],
                     state='readonly') \
            .grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(jj, text="结界卡").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(jj, textvariable=dkConfigs["结界卡"],
                     values=["全部", "太鼓", "斗鱼", "伞室内", "太阴符咒", "特殊变异"], state='readonly') \
            .grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(jj, text="星级").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(jj, text="降序", value="降序", variable=dkConfigs["结界卡排序"]) \
            .grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(jj, text="升序", value="升序", variable=dkConfigs["结界卡排序"]) \
            .grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        jj.grid(row=0, column=0, sticky=tk.NW, pady=2)

        jjtp = ttk.LabelFrame(row4, text="结界突破", padding=10)
        ttk.Checkbutton(jjtp, text="个人突破", offvalue=0, onvalue=1, variable=dkConfigs["个人突破"]) \
            .grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Checkbutton(jjtp, text="寮突破", offvalue=0, onvalue=1, variable=dkConfigs["寮突破"]) \
            .grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(jjtp, text="结界突破绿标位置").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(jjtp, textvariable=dkConfigs["突破绿标式神位"], values=["0", "1", "2", "3", "4", "5"],
                     state='readonly').grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        jjtp.grid(row=0, column=1, sticky=tk.NW, pady=2, padx=10)
        row4.grid(row=3, column=0, sticky=tk.W, pady=2)

        row5 = tk.Frame(tab)
        ts = ttk.LabelFrame(row5, text="探索", padding=10)
        ttk.Checkbutton(ts, text="开启", offvalue=0, onvalue=1, variable=dkConfigs["探索"]) \
            .grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(ts, text="次数")\
            .grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Entry(ts, textvariable=dkConfigs["探索次数"])\
            .grid(row=0, column=2, padx=5)
        ts.grid(row=0, column=0, sticky=tk.W, pady=2)
        row5.grid(row=4, column=0, sticky=tk.W, pady=2)

    def regTab3(self, tab):
        logger.info("组队刷刷尚未制作")

    def regTab4(self, tab):
        hdConfigs = self.configs.configs["活动模式"]

        ttk.Checkbutton(tab, text="开启", offvalue=0, onvalue=1, variable=hdConfigs["开启"]) \
            .grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(tab, text="活动次数") \
            .grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Entry(tab, textvariable=hdConfigs["次数"]) \
            .grid(row=0, column=2, sticky=tk.W, padx=5)

    # Tab: 使用说明
    @staticmethod
    def regTipsTab(tab):
        tips = tk.Text(tab)
        tips.pack(fill="both")
        file = open(os.getcwd() + "\\tips.txt", "r", encoding="utf-8")
        for txt in file:
            tips.insert("insert", txt)
        file.close()

    # Tab: 更新日志
    @staticmethod
    def regUpdateTab(tab):
        update = tk.Text(tab)
        update.pack(fill="both")
        file = open(os.getcwd() + "\\update.txt", "r", encoding="utf-8")
        for txt in file:
            update.insert("insert", txt)
        file.close()

    def clock(self, root, label):
        now = datetime.now()
        if now.strftime("%H:%M:%S") == "00:00:00":
            config.Config().clearDaily()
            logger.info("[时钟] 清理日常任务记录")
        elif now.strftime("%H:%M:%S") == "06:00:00":
            script.setInfo("寮突破今日目标", "进行中")
            logger.info("[时钟] 重置寮突破今日目标")
        self.now = now.strftime("%Y-%m-%d %H:%M:%S")
        label.configure(text=self.now)
        root.after(1000, self.clock, root, label)

    def running(self, root, label):
        running = script.getRunning()
        bg = "white"
        if running == "未开始":
            bg = "blue"
        elif running == "暂停":
            bg = "red"
        elif running == "运行中":
            bg = "green"
        label.configure(text=running, background=bg)
        root.after(100, self.running, root, label)

    def getScriptStatus(self, root, label, key):
        label.configure(text=script.getInfo(key))
        root.after(100, self.getScriptStatus, root, label, key)


class HotkeyThread(Thread):  # 创建一个Thread.threading的扩展类
    f10 = 121
    f11 = 122

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # 注册快捷键F10并判断是否成功
        if not user32.RegisterHotKey(None, self.f10, 0, win32con.VK_F10):
            messagebox.showerror("注册热键失败", "F10 热键注册失败, 请检查是否被占用")
        if not user32.RegisterHotKey(None, self.f11, 0, win32con.VK_F11):
            messagebox.showerror("注册热键失败", "F11 热键注册失败, 请检查是否被占用")

        try:
            # 监听热键
            msg = ctypes.wintypes.MSG()
            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == self.f10:
                            script.run()
                        if msg.wParam == self.f11:
                            script.restart()

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            # 释放热键
            user32.UnregisterHotKey(None, "F10")
            user32.UnregisterHotKey(None, "F11")


if __name__ == "__main__":
    # 注册线程
    script.newThread()

    # 注册快捷键
    hotkeyThread = HotkeyThread()
    hotkeyThread.daemon = True
    hotkeyThread.start()

    # 注册界面
    tkinter = tk.Tk()
    app = App(tkinter)

    # 注册日志监听
    logger.init(app)

    # 启动助手界面
    tkinter.mainloop()
