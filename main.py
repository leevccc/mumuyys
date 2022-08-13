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
    path = os.getcwd() + "\\img\\"
    window = 2
    init = 0
    clients = 1
    window_info = []

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

        x = self.x
        y = self.y
        rx = self.x + self.weight
        ry = self.y + self.height

        # 截图前把鼠标移除出游戏界面
        mouse_x, mouse_y = pyautogui.position()
        if x < mouse_x < rx and y < mouse_y < ry:
            pyautogui.moveTo(rx, ry)

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

    def switch_window(self, num=None):
        """
        切换窗口

        :param num: 切换到第 num 个模拟器窗口, 不填默认为下个窗口
        """
        if num is None:
            num = self.window + 1
        num = int(num)
        if num < 1 or num > 9:
            num = 2
        pyautogui.hotkey("ctrl", str(num))
        self.window = num
        self.syslog("切换到窗口 " + str(num))

    def log(self, text, window=None):
        if window is None:
            window = self.window
        now = datetime.now()
        module_logger.info("%s [窗口%s]: %s" % (now.strftime("%H:%M:%S"), window, text))

    def syslog(self, text):
        now = datetime.now()
        self.log_tag = "sys"
        module_logger.info("%s (系统): %s" % (now.strftime("%H:%M:%S"), text))
        self.log_tag = None

    def run_task(self, setting_section, setting_key, task_func, msg=True, daily=False):
        if daily and self.app.get_daily_record(self.window, setting_key) == "finish":
            self.log("[任务] %s 今日已完成,跳过" % setting_key)
            return
        if self.app.settings[setting_section][setting_key].get() == 1:
            if msg:
                self.log("[任务] %s" % setting_key)
            task_func()
            if daily:
                # 每日任务完成标记
                self.app.set_daily_record(self.window, setting_key, "finish")

    def task_qiandao(self):
        if self.find_pic("qiandao.jpg", click=True):
            self.find_pic("qiandao2.jpg", click=True, times=30)
            self.random_sleep(2000, 1500)
            self.find_pic("close.jpg", click=True, times=10)

    def task_huang_jin_qiandao(self):
        if self.find_pic("huangjinqiandao.jpg", click=True):
            self.random_sleep()
            self.click_100()

    def task_mail(self):
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

    def task_you_qing_dian(self):
        self.click(964, 686, 62, 68)
        if self.find_pic("youqingdian.jpg", click=True, times=4):
            if self.find_pic("yijianlingqu.jpg", click=True, times=4):
                self.random_sleep()
                self.click_100()
        self.action_hui_ting_yuan()

    def task_liao_zi_jin(self):
        self.click(530, 674, 66, 73)
        if self.find_pic("zijinlingqu.jpg", click=True, confidence=0.99, times=4):
            if self.find_pic("lingqu.jpg", click=True, times=4):
                self.random_sleep()
                self.click_100()
        self.action_hui_ting_yuan()

    def action_ting_yuan_shou_si(self):
        if self.find_pic("shousi.jpg", confidence=0.95, click=True):
            self.log("[动作] 领取庭院寿司")
            self.random_sleep()
            self.click_100()

    def action_ting_yuan_gou_yu(self):
        if self.find_pic("gouyu.jpg", click=True):
            self.log("[动作] 领取庭院勾玉")
            self.random_sleep()
            self.click_100()

    def action_ting_yuan_yu_hun(self):
        if self.find_pic("yuhun.jpg", click=True):
            self.log("[动作] 领取庭院御魂")
            self.find_pic("querenlingqu.jpg", click=True, times=4)
            self.random_sleep()
            self.click_100()

    def action_hui_ting_yuan(self):
        button = [
            "close2.jpg",
            "fanhui.jpg",
            "fanhui2.jpg",
        ]

        i = 0
        while self.zt_zai_ting_yuan() is False:
            self.log("[动作] 回庭院")
            self.find_pic(button[i], click=True)
            i += 1
            if i == len(button):
                i = 0
            time.sleep(1)

    def action_kai_juan_zhou(self):
        if self.find_pic("tingyuanjuanzhou.jpg", click=True):
            self.log("[动作] 开启底部导航卷轴")

    def zt_zai_ting_yuan(self):
        """
        判断是否在庭院

        :return: True / False
        """
        x, y = self.find_pic("feng.jpg")
        if x is not None:
            self.log("[状态] 在庭院")
            self.run_task("日常任务", "领取庭院寿司", self.action_ting_yuan_shou_si, False)
            self.run_task("日常任务", "领取庭院勾玉", self.action_ting_yuan_gou_yu, False)
            self.run_task("日常任务", "领取庭院御魂", self.action_ting_yuan_yu_hun, False)
            return True
        else:
            return False

    def task(self):
        while True:
            if self.task_status:
                times = self.clients
                while times > 0:
                    if self.zt_zai_ting_yuan():
                        self.action_kai_juan_zhou()
                        self.run_task("日常任务", "每日签到", self.task_qiandao, daily=True)
                        self.run_task("日常任务", "黄金签到", self.task_huang_jin_qiandao, daily=True)
                        self.run_task("日常任务", "领取邮件", self.task_mail, daily=True)
                        self.run_task("日常任务", "领取黑蛋", self.task_shang_dian_fu_li, daily=True)
                        self.run_task("日常任务", "友情点", self.task_you_qing_dian, daily=True)
                        self.run_task("日常任务", "领取寮资金", self.task_liao_zi_jin, daily=True)

                    times -= 1
                    if 1 < self.clients and (self.window - 1) < self.clients:
                        # 最大客户端数大于 1 且当前窗口未超出客户端范围, 切换到下个窗口
                        self.switch_window()

                self.log("所有任务执行完毕")
                self.run()
                self.init = 0

    def run(self):
        if self.task_status:
            self.syslog("暂停脚本")
            self.app.start_button_text.set("运行 F10")
            self.task_status = False
        else:
            self.init_mumu_window()
            if self.init == 0:
                self.clients = app.settings['基本设置']['客户端数'].get()
                self.window_info = []
                # 多开, 重置窗口为第一个游戏窗口
                if self.clients > 1:
                    self.switch_window(2)
                self.init = 1
            self.syslog("运行脚本")
            self.app.start_button_text.set("暂停 F10")
            self.task_status = True

    @staticmethod
    def kill(msg):
        messagebox.showinfo('提示', msg)
        sys.exit(0)

    def set_app(self, obj):
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
        self.app.log.see("end")
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
            self.script_obj.log("F10 热键注册失败, 请检查是否被占用")
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
    conf = None
    script_obj = None
    width = None
    height = None
    log = None
    start_button_text = None
    stop_button_text = None
    settings_list = {
        "日常任务": {
            "Daily": [
                "每日签到",
                "黄金签到",
                "领取邮件",
                "领取黑蛋",
                "友情点",
                "领取寮资金",
            ],
            "TingYuan": [
                "领取庭院寿司",
                "领取庭院勾玉",
                "领取庭院御魂",
            ],
        },
    }
    settings = {}

    def __init__(self, root, script_obj):
        # setting 值初始化
        self.script_obj = script_obj
        self.init_setting()

        # 将 app 注册到 script, 允许 script 修改 app 按钮文字
        script_obj.set_app(self)

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

        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="日志信息")
        self.init_tab1(tab1)

        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="基本设置")
        tab2.config(padx=10, pady=10)
        self.init_tab2(tab2)

        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="日常任务")
        tab3.config(padx=10, pady=10)
        self.init_tab3(tab3)

        notebook.pack(expand=True, fill=tk.BOTH)

    def save_settings(self):
        for _key in self.settings:
            if self.conf.has_section(_key) is False:
                self.conf.add_section(_key)
            for __key in self.settings[_key]:
                self.conf.set(_key, __key, str(self.settings[_key][__key].get()))
        self.conf.write(open('config.ini', 'w'))

    def load_settings(self):
        self.conf = ConfigParser()
        self.conf.read('config.ini')
        if len(self.conf.sections()) == 0:
            return

        for _key in self.settings:
            if self.conf.has_section(_key) is False:
                continue
            for __key in self.settings[_key]:
                if self.conf.has_option(_key, __key):
                    try:
                        self.settings[_key][__key].set(self.conf.getint(_key, __key))
                    except ValueError:
                        self.settings[_key][__key].set(self.conf.get(_key, __key))

        self.clear_conf_daily_record()

    def set_conf(self, section, key, val):
        if self.conf.has_section(section) is False:
            self.conf.add_section(section)
        self.conf.set(section, key, val)
        self.conf.write(open('config.ini', 'w'))

    def get_conf(self, section, key):
        result = None
        if self.conf.has_section(section) and self.conf.has_option(section, key):
            result = self.conf.get(section, key)
        return result

    def clear_conf_daily_record(self):
        now = datetime.now()
        today = now.strftime("%Y%m%d")
        if self.conf.has_section("DailyRecord"):
            if self.conf.get("DailyRecord", "date") != today:
                self.conf.remove_section("DailyRecord")
                self.conf.add_section("DailyRecord")
                self.conf.set("DailyRecord", "date", today)
        else:
            self.conf.add_section("DailyRecord")
            self.conf.set("DailyRecord", "date", today)

    def get_daily_record(self, window, key):
        opt = "window_%s_%s" % (window, key)
        return self.get_conf("DailyRecord", opt)

    def set_daily_record(self, window, key, val):
        opt = "window_%s_%s" % (window, key)
        self.set_conf("DailyRecord", opt, val)

    def init_setting(self):
        self.settings["基本设置"] = {}
        self.settings["基本设置"]["客户端数"] = tk.IntVar()
        self.settings["基本设置"]["客户端数"].set(1)
        self.settings["日常任务"] = {}
        for value in self.settings_list["日常任务"]["Daily"]:
            self.settings["日常任务"][value] = tk.IntVar()
            self.settings["日常任务"][value].set(1)
        for value in self.settings_list["日常任务"]['TingYuan']:
            self.settings["日常任务"][value] = tk.IntVar()
            self.settings["日常任务"][value].set(1)

        # 加载本地配置
        self.load_settings()

    # Tab: 日志信息
    def init_tab1(self, tab):
        # 日志
        self.log = tk.Text(tab, state="disabled", padx=0, pady=0)
        self.log.place(x=-1, y=-1, width=self.width, height=400)
        # 设置系统日志样式 tag
        self.log.tag_add("sys", "end")
        self.log.tag_config("sys", foreground="blue", background="pink")

        # 日志页 - 底部按钮
        self.start_button_text = tk.StringVar()
        self.start_button_text.set("运行 F10")
        tk.Button(tab, textvariable=self.start_button_text, command=lambda: self.script_obj.run()) \
            .place(x=200, y=420, width=80, height=30)

        self.stop_button_text = tk.StringVar()
        self.stop_button_text.set("结束")
        tk.Button(tab, textvariable=self.stop_button_text, command=lambda: self.script_obj.kill("手动结束")) \
            .place(x=320, y=420, width=80, height=30)

    # Tab: 基本设置
    def init_tab2(self, tab):
        tk.Label(tab, text="客户端数", anchor='e').place(x=0, y=0, width=60, height=20)
        tk.Radiobutton(tab, text="单开", value=1, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=60, y=0, width=50, height=20)
        tk.Radiobutton(tab, text="双开", value=2, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=110, y=0, width=50, height=20)
        tk.Radiobutton(tab, text="三开", value=3, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=160, y=0, width=50, height=20)
        # 底部 配置按钮
        tk.Button(tab, text="保存配置", command=lambda: self.save_settings()) \
            .place(x=190, y=410, width=80, height=30)
        tk.Button(tab, text="读取配置", command=lambda: self.load_settings()) \
            .place(x=310, y=410, width=80, height=30)

    # 日常任务
    def init_tab3(self, tab):
        daily = tk.LabelFrame(tab, text="每日一次")
        daily.place(x=0, y=0, width=130, height=200)
        for i, val in enumerate(self.settings_list["日常任务"]['Daily']):
            tk.Checkbutton(daily,
                           text=val, anchor="w",
                           offvalue=0, onvalue=1,
                           variable=self.settings["日常任务"][val]) \
                .place(x=0, y=i * 30, width=120, height=20)

        ting_yuan = tk.LabelFrame(tab, text="回庭院时监测")
        ting_yuan.place(x=0, y=210, width=130, height=110)
        for i, val in enumerate(self.settings_list["日常任务"]['TingYuan']):
            tk.Checkbutton(ting_yuan,
                           text=val, anchor="w",
                           offvalue=0, onvalue=1,
                           variable=self.settings["日常任务"][val]) \
                .place(x=0, y=i * 30, width=120, height=20)


if __name__ == "__main__":
    # 实例化脚本
    script = Script()

    # 获取模拟器窗口句柄
    script.get_hwnd()

    # 注册线程
    main_thread = TaskThread(script)
    main_thread.daemon = True
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
    hotkey.daemon = True
    hotkey.start()

    # 启动助手界面
    tkinter.mainloop()
