import logging
import os
import sys
import time
import tkinter as tk
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


class MyThread(Thread):
    def __init__(self, name, script_obj):
        Thread.__init__(self)
        self.name = name
        self.script_obj = script_obj

    def run(self):
        print("开启线程： " + self.name)
        self.script_obj.task()


class Script:
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
        window = win32gui.FindWindow(0, "阴阳师 - MuMu模拟器")
        if window == 0:
            print("找不到游戏窗口, 脚本退出")
            sys.exit(0)
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
        print("坐标:", "宽", right, "高", bottom, "顶", top, "左", left, "分辨率 1440 x 810")

    def print_screen(self):
        """
        窗口截图
        """
        # app = QApplication(sys.argv)
        # screen = QApplication.primaryScreen()
        # img = screen.grabWindow(self.hwnd).toImage()
        # url = self.path + "\\img\\screenshot.jpg"
        # img.save(url)
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
        :return: x , y 坐标
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
            return None, None

        x, y = match_result["result"]
        if click:
            x = match_result["rectangle"][0][0]
            y = match_result["rectangle"][0][1]
            width = match_result["rectangle"][3][0] - x
            height = match_result["rectangle"][3][1] - y
            self.click(x, y, width, height)

        return int(x), int(y)

    def click(self, x, y, width, height):
        """
        模拟鼠标点击

        :param x: 横坐标
        :param y: 纵坐标
        :param width: 横坐标偏移量
        :param height: 纵坐标偏移量
        """
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
        module_logger.info("[窗口%s](%s): %s" % (window, now.strftime("%H:%M:%S"), text))

    def task_kai_juan_zhou(self):
        self.log("自动开启底部导航卷轴")
        self.find_pic("tingyuanjuanzhou.jpg", click=True)

    def task_qiandao(self):
        self.log("执行签到任务")
        if self.find_pic("qiandao.jpg", click=True)[0] is not None:
            self.find_pic("qiandao2.jpg", click=True, times=30)
            self.find_pic("close.jpg", click=True, times=10)

    def zt_zai_ting_yuan(self):
        x, y = self.find_pic("feng.jpg")
        if x is not None:
            self.log("在庭院")
            return True
        else:
            return False

    def task(self):
        while True:
            if self.task_status:
                if self.zt_zai_ting_yuan():
                    self.task_kai_juan_zhou()
                    self.task_qiandao()
                self.log("所有任务执行完毕")
                self.task_status = False

    def run(self):
        self.task_status = True

    def stop(self):
        self.task_status = False


class HandlerLog(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self)
        App.log = textctrl

    def emit(self, record):
        msg = self.format(record)
        App.log.config(state="normal")
        App.log.insert("end", msg + "\n")
        App.log.update()
        App.log.config(state="disabled")


class App:
    log = None

    def __init__(self, root, script_object):
        # 设置窗口title
        root.title("mumu阴阳师助手")

        # 设置窗口大小:宽x高
        # root.geometry("400x600")
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(align_str)
        root.resizable(width=False, height=False)

        # 功能区
        self.log = tk.Text(root, state="disabled", background="#FFF", borderwidth=1)
        self.log.place(x=300, y=10, width=300, height=430)

        # 底部按钮
        self.start_button_text = tk.StringVar()
        self.start_button_text.set("启动")
        start_button = tk.Button(root, textvariable=self.start_button_text, command=lambda: script_object.run())
        start_button.place(x=200, y=450, width=80, height=30)

        self.stop_button_text = tk.StringVar()
        self.stop_button_text.set("结束")
        stop_button = tk.Button(root, textvariable=self.stop_button_text, command=lambda: script_object.stop())
        stop_button.place(x=320, y=450, width=80, height=30)


if __name__ == "__main__":
    # 实例化脚本
    script = Script()

    # 获取模拟器窗口句柄
    script.get_hwnd()

    # 初始化模拟器窗口
    script.init_mumu_window()

    main_thread = MyThread('主程序', script)
    main_thread.setDaemon(True)
    main_thread.start()

    # 注册助手
    tkinter = tk.Tk()
    app = App(tkinter, script)

    # 注册日志监听
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = HandlerLog(app.log)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)

    tkinter.mainloop()
