import ctypes
import ctypes.wintypes
import logging
import os
import sys
import time
import tkinter as tk
from configparser import ConfigParser

from ttkbootstrap import ttk
import tkinter.messagebox as messagebox
from datetime import datetime
from random import random
from threading import Thread

import aircv
import pyautogui
# python -m pip install pypiwin32
# pip install pywin32
import win32con
import win32gui

module_logger = logging.getLogger(__name__)
user32 = ctypes.windll.user32  # 加载user32.dll


class Script:
    app = None
    log_tag = None
    task_status = False
    x = None
    y = None
    weight = 1440
    height = 810
    hwnd = None
    path = os.path.split(os.path.realpath(__file__))[0] + "\\img\\"
    window = 2

    # 初始化
    # def __init__(self):

    def get_hwnd(self):
        """
        获取 MuMu 窗口句柄
        """
        window = 0
        max_times = 3
        for i in range(0, max_times):
            window_title = "阴阳师 - MuMu模拟器"
            if i > 0:
                window_title = "#N" + str(i) + " 阴阳师 - MuMu模拟器"
            window = win32gui.FindWindow(0, window_title)
            if window != 0:
                break

        if window == 0:
            self.kill("找不到游戏窗口, 脚本退出")
        self.hwnd = window
        return window

    def init_mumu_window(self):
        """
        调整模拟器位置和大小
        """
        # 还原窗口
        win32gui.SendMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        # 激活窗口
        win32gui.SetForegroundWindow(self.hwnd)
        # 设置窗口位置和大小 宽 1440 高 899(含标题36 底部工具栏53) 实际分辨率 1440 x 810
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOP, 0, 0, 1440, 899, win32con.SWP_SHOWWINDOW)
        # 获取窗口位置参数
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.x = left
        self.y = top + 36
        self.syslog("窗口坐标: 宽 " + str(right) + " 高 " + str(bottom) + " 顶 " + str(top) + " 左 " + str(
            left) + " 分辨率 1440 x 810")

    def print_screen(self):
        """
        窗口截图
        """
        # app = QApplication(sys.argv)
        # screen = QApplication.primaryScreen()
        # img = screen.grabWindow(self.hwnd).toImage()
        # url = self.path + "\\img\\screenshot.jpg"
        # img.save(url)

        # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
        while self.task_status is False:
            time.sleep(1)

        pyautogui.moveTo(100, 10)
        x = self.x
        y = self.y
        rx = self.x + self.weight
        ry = self.y + self.height
        screen = pyautogui.screenshot(region=(x, y, rx, ry))
        screen.save(self.path + "\\temp\\screenshot.jpg")

    def find_pic(self, path, confidence=0.8, click=False, times=1):
        """
        查找图片, 每隔 0.5 秒读取一次

        :param path: 图片相对地址
        :param confidence: 匹配度
        :param click: 识别后是否点击
        :param times: 次数
        :return: 按匹配结果依次返回: 失败 - None, None; 成功 - int(x), int(Y); 成功且需要点击 - True
        """
        match_result = None
        for i in range(0, times):
            Script.print_screen(self)
            screenshot = aircv.imread(self.path + "\\temp\\screenshot.jpg")
            img = aircv.imread(self.path + path)

            match_result = aircv.find_template(screenshot, img, confidence)
            # match_result
            # {
            #   'result': (1335.0, 731.5),
            #   'rectangle': ((1298, 682), (1298, 781), (1372, 682), (1372, 781)),
            #   'confidence': 0.993413507938385
            # }

            if match_result is None:
                time.sleep(0.5)
                continue
            else:
                break

        if match_result is None:
            return False if click is True else (None, None)

        x, y = match_result["result"]
        if click:
            x = match_result["rectangle"][0][0]
            y = match_result["rectangle"][0][1]
            width = match_result["rectangle"][3][0] - x
            height = match_result["rectangle"][3][1] - y
            self.click(x, y, width, height)
            return True

        return int(x), int(y)

    def click(self, x, y, width, height):
        """
        模拟鼠标点击

        :param x: 横坐标
        :param y: 纵坐标
        :param width: 横坐标偏移量
        :param height: 纵坐标偏移量
        """
        # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
        while self.task_status is False:
            time.sleep(1)

        x = self.x + x
        y = self.y + y
        pyautogui.moveTo(x + self.random_max(width), y + self.random_max(height))
        Script.random_sleep()
        pyautogui.click()

    def click_100(self):
        self.click(10, 10, 190, 90)

    @staticmethod
    def random_max(num):
        """
        返回 0 ~ max 的随机数

        :param num: 最大值
        :return:
        """
        return round(random() * num)

    @staticmethod
    def random_sleep(max_sleep=1000, min_sleep=500):
        """
        随机延迟 min ~ max 毫秒, 如果 min > max 则重设 max = min + 500

        :param max_sleep: 最大毫秒
        :param min_sleep: 最小毫秒
        """
        if min_sleep > max_sleep:
            max_sleep = min_sleep + 500

        sleep = min_sleep + round(random() * (max_sleep - min_sleep))
        time.sleep(sleep / 1000)

    @staticmethod
    def switch_window(num):
        """
        切换窗口

        :param num: 切换到第 num 个模拟器窗口, 默认第一个游戏窗口为 2
        """
        num = int(num)
        if num < 1 or num > 9:
            num = 2
        pyautogui.hotkey("ctrl", str(num))

    @staticmethod
    def log(text, window=window):
        now = datetime.now()
        module_logger.info("%s [窗口%s]: %s" % (now.strftime("%H:%M:%S"), window, text))

    def syslog(self, text):
        now = datetime.now()
        self.log_tag = "sys"
        module_logger.info("%s (系统): %s" % (now.strftime("%H:%M:%S"), text))
        self.log_tag = None

    def task_kai_juan_zhou(self):
        self.log("自动开启底部导航卷轴")
        self.find_pic("tingyuanjuanzhou.jpg", click=True)

    def task_qiandao(self):
        self.log("[任务] 签到")
        if self.find_pic("qiandao.jpg", click=True):
            self.find_pic("qiandao2.jpg", click=True, times=30)
            self.random_sleep(2000, 1500)
            self.find_pic("close.jpg", click=True, times=10)

    def task_huang_jin_qiandao(self):
        self.log("[任务] 黄金签到")
        if self.find_pic("huangjinqiandao.jpg", click=True):
            self.random_sleep()
            self.click_100()

    def task_mail(self):
        self.log("[任务] 收取邮件")
        if self.find_pic("mail.jpg", click=True):
            if self.find_pic("receivemail.jpg", click=True, times=6):
                if self.find_pic("confirm.jpg", click=True, times=6):
                    self.random_sleep(1500, 1000)
                    self.click_100()
                    self.action_hui_ting_yuan()
                else:
                    self.kill("找不到确认按钮")
            else:
                self.log("没有邮件, 返回庭院")
                self.action_hui_ting_yuan()

    def task_shang_dian_fu_li(self):
        self.log("[任务] 领取商店每日福利")
        self.log("进入商店")
        self.click(685, 684, 50, 60)

        self.log("关闭推荐按钮")
        self.find_pic("close.jpg", click=True, times=4)

        self.log("进入礼包屋")
        self.click(1300, 714, 60, 60)

        self.log("点击黑蛋")
        if self.find_pic("mianfei.jpg", click=True, times=6) is False:
            self.find_pic("tuijian.jpg", click=True)
            self.find_pic("mianfei.jpg", click=True, times=6)
        self.random_sleep(1500, 1000)
        self.click_100()
        self.action_hui_ting_yuan()

    def task_ting_yuan_shou_si(self):
        self.log("[任务] 庭院寿司")
        if self.find_pic("shousi.jpg", confidence=0.95, click=True):
            self.random_sleep()
            self.click_100()

    def task_ting_yuan_gou_yu(self):
        self.log("[任务] 庭院勾玉")
        if self.find_pic("gouyu.jpg", click=True):
            self.random_sleep()
            self.click_100()

    def task_you_qing_dian(self):
        self.log("[任务] 友情点")
        self.click(964, 686, 62, 68)
        if self.find_pic("youqingdian.jpg", click=True, times=4):
            if self.find_pic("yijianlingqu.jpg", click=True, times=4):
                self.random_sleep()
                self.click_100()
        self.action_hui_ting_yuan()

    def task_liao_zi_jin(self):
        self.log("[任务] 寮资金领取")
        self.click(530, 674, 66, 73)
        if self.find_pic("zijinlingqu.jpg", click=True, confidence=0.98, times=4):
            if self.find_pic("lingqu.jpg", click=True, times=4):
                self.random_sleep()
                self.click_100()
        self.action_hui_ting_yuan()

    def zt_zai_ting_yuan(self):
        """
        判断是否在庭院

        :return: True / False
        """
        x, y = self.find_pic("feng.jpg")
        if x is not None:
            self.log("[状态] 在庭院")
            return True
        else:
            return False

    def action_hui_ting_yuan(self):
        self.log("[动作] 回庭院")
        button = [
            "close2.jpg",
            "fanhui.jpg",
            "fanhui2.jpg",
        ]

        i = 0
        while self.zt_zai_ting_yuan() is False:
            self.find_pic(button[i], click=True)
            i += 1
            if i == len(button):
                i = 0
            time.sleep(1)

    def task(self):
        while True:
            if self.task_status:
                if self.zt_zai_ting_yuan():
                    self.task_ting_yuan_shou_si()
                    self.task_kai_juan_zhou()
                    self.task_mail()
                    self.task_shang_dian_fu_li()
                    self.task_qiandao()
                    self.task_ting_yuan_gou_yu()
                    self.task_huang_jin_qiandao()
                    self.task_you_qing_dian()
                    self.task_liao_zi_jin()
                self.log("所有任务执行完毕")
                self.run()

    def run(self):
        if self.task_status:
            self.syslog("暂停脚本")
            self.app.start_button_text.set("运行 F10")
            self.task_status = False
        else:
            self.init_mumu_window()
            self.syslog("运行脚本")
            self.app.start_button_text.set("暂停 F10")
            self.task_status = True

    @staticmethod
    def kill(msg):
        messagebox.showinfo('提示', msg)
        sys.exit(0)

    def setApp(self, obj):
        self.app = obj


class HandlerLog(logging.StreamHandler):
    def __init__(self, app_obj):
        logging.StreamHandler.__init__(self)
        self.app = app_obj

    def emit(self, record):
        msg = self.format(record)
        self.app.log.config(state="normal")
        self.app.log.insert("end", msg + "\n", script.log_tag)
        self.app.log.update()
        self.app.log.config(state="disabled")


class TaskThread(Thread):
    def __init__(self, script_obj):
        Thread.__init__(self)
        self.script_obj = script_obj

    def run(self):
        self.script_obj.task()


class HotkeyThread(Thread):  # 创建一个Thread.threading的扩展类
    f10 = 121

    def __init__(self, script_obj):
        Thread.__init__(self)
        self.script_obj = script_obj

    def run(self):
        # 注册快捷键F10并判断是否成功
        if not user32.RegisterHotKey(None, self.f10, 0, win32con.VK_F10):
            Script.log("F10 热键注册失败, 请检查是否被占用")
            messagebox.showerror("注册热键失败", "F10 热键注册失败, 请检查是否被占用")

        try:
            # 监听热键
            msg = ctypes.wintypes.MSG()
            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == self.f10:
                            Script.run(self.script_obj)

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            # 释放热键
            user32.UnregisterHotKey(None, "F10")


class App:
    script_obj = None
    width = None
    height = None
    tab1 = None
    tab2 = None
    log = None
    start_button_text = None
    stop_button_text = None
    settings = {}

    def __init__(self, root, script_obj):
        # setting 值初始化
        self.script_obj = script_obj
        self.initSetting()

        # 将 app 注册到 script, 允许 script 修改 app 按钮文字
        script_obj.setApp(self)

        # 助手界面
        root.title("mumu阴阳师助手")
        self.width = 600
        self.height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % \
                    (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        root.geometry(align_str)
        root.resizable(width=False, height=False)

        # 标签页
        notebook = ttk.Notebook(root)

        self.tab1 = tk.Frame(notebook)
        notebook.add(self.tab1, text="日志信息")
        self.initTab1()

        self.tab2 = tk.Frame(notebook)
        notebook.add(self.tab2, text="基本设置")
        self.tab2.config(padx=10, pady=10)
        self.initTab2()

        notebook.pack(expand=True, fill=tk.BOTH)

    def saveSettings(self):
        conf = ConfigParser()
        conf.read('config.ini')

        for _key in self.settings:
            if conf.has_section(_key) is False:
                conf.add_section(_key)
            for __key in self.settings[_key]:
                conf.set(_key, __key, self.settings[_key][__key].get())
        conf.write(open('config.ini', 'w'))

    def loadSettings(self):
        conf = ConfigParser()
        conf.read('config.ini')
        if len(conf.sections()) == 0:
            return

        for _key in self.settings:
            if conf.has_section(_key) is False:
                continue
            for __key in self.settings[_key]:
                if conf.get(_key, __key):
                    self.settings[_key][__key].set(conf.get(_key, __key))

    def initSetting(self):
        self.settings["基本设置"] = {}
        self.settings["基本设置"]["客户端数"] = tk.StringVar()
        self.settings["基本设置"]["客户端数"].set("1")

    # Tab: 日志信息
    def initTab1(self):
        # 日志
        self.log = tk.Text(self.tab1, state="disabled", padx=0, pady=0)
        self.log.place(x=-1, y=-1, width=self.width, height=400)
        # 设置系统日志样式 tag
        self.log.tag_add("sys", "end")
        self.log.tag_config("sys", foreground="blue", background="pink")

        # 日志页 - 底部按钮
        self.start_button_text = tk.StringVar()
        self.start_button_text.set("运行 F10")
        tk.Button(self.tab1, textvariable=self.start_button_text, command=lambda: self.script_obj.run()) \
            .place(x=200, y=420, width=80, height=30)

        self.stop_button_text = tk.StringVar()
        self.stop_button_text.set("结束")
        tk.Button(self.tab1, textvariable=self.stop_button_text, command=lambda: self.script_obj.kill("手动结束")) \
            .place(x=320, y=420, width=80, height=30)

    # Tab: 基本设置
    def initTab2(self):
        tk.Button(self.tab2, text="保存配置", command=lambda: self.saveSettings()).grid(row=0, column=0)
        tk.Button(self.tab2, text="读取配置", command=lambda: self.loadSettings()).grid(row=0, column=2)
        tk.Label(self.tab2, text="客户端数").grid(row=1, column=0)
        print(self.settings)
        tk.Radiobutton(self.tab2, text="单开", value="1", variable=self.settings["基本设置"]["客户端数"]) \
            .grid(row=1, column=1)
        tk.Radiobutton(self.tab2, text="双开", value="2", variable=self.settings["基本设置"]["客户端数"]) \
            .grid(row=1, column=2)
        tk.Radiobutton(self.tab2, text="三开", value="3", variable=self.settings["基本设置"]["客户端数"]) \
            .grid(row=1, column=3)


if __name__ == "__main__":
    # 实例化脚本
    script = Script()

    # 获取模拟器窗口句柄
    script.get_hwnd()

    # 注册线程
    main_thread = TaskThread(script)
    main_thread.setDaemon(True)
    main_thread.start()

    # 注册助手界面
    tkinter = tk.Tk()
    app = App(tkinter, script)

    # 注册日志监听
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = HandlerLog(app)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)
    module_logger.info("[日志信息]")

    # 注册快捷键
    hotkey = HotkeyThread(script)
    hotkey.setDaemon(True)
    hotkey.start()

    # 启动助手界面
    tkinter.mainloop()
