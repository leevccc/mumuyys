import os
import sys
import time
import tkinter as tk
from random import random
from threading import Thread

import aircv
import pyautogui
# python -m pip install pypiwin32
# pip install pywin32
import win32con
import win32gui


class MyThread(Thread):
    def __init__(self, name, script_obj):
        Thread.__init__(self)
        self.name = name
        self.script_obj = script_obj

    def run(self):
        print("开启线程： " + self.name)
        self.script_obj.task(self.name)


class Script:
    # 初始化
    def __init__(self):
        self.task_status = False
        self.x = None
        self.y = None
        self.weight = 1440
        self.height = 810
        self.hwnd = None
        self.path = os.path.split(os.path.realpath(__file__))[0]

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
        screen.save(self.path + "\\img\\screenshot.jpg")

    def find_pic(self, path, confidence=0.8):
        """
        查找图片

        :param path: 图片相对地址
        :param confidence: 匹配度
        :return: x , y 坐标
        """
        Script.print_screen(self)
        screenshot = aircv.imread(self.path + "\\img\\screenshot.jpg")
        img = aircv.imread(self.path + path)

        match_result = aircv.find_template(screenshot, img, confidence)
        # 返回是个字典 result 是中心坐标
        x, y = match_result["result"]

        return int(x), int(y)

    @staticmethod
    def click(x, y):
        """
        模拟鼠标点击

        :param x: 横坐标
        :param y: 纵坐标
        """
        pyautogui.moveTo(x, y)
        Script.random_sleep(500)
        pyautogui.click()

    @staticmethod
    def random_sleep(max_sleep, min_sleep=0):
        """
        随机延迟 min ~ max 毫秒, 如果 min > max 则重设 max = min + 1000

        :param max_sleep: 最大毫秒
        :param min_sleep: 最小毫秒
        """
        if min_sleep > max_sleep:
            max_sleep = min_sleep + 1000

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

    def task(self, thread_name):
        for i in range(0, 10):
            print("%s: %s" % (thread_name, time.ctime(time.time())))
            time.sleep(2)
            if self.task_status:
                print(i)
                i += 1

    def run(self):
        self.task_status = True

    def stop(self):
        self.task_status = False


class App:
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

        # 底部按钮
        Script.start_button_text = tk.StringVar()
        Script.start_button_text.set("启动")
        start_button = tk.Button(root, textvariable=Script.start_button_text, command=lambda: script_object.run())
        start_button.place(x=200, y=450, width=80, height=30)

        Script.stop_button_text = tk.StringVar()
        Script.stop_button_text.set("结束")
        stop_button = tk.Button(root, textvariable=Script.stop_button_text, command=lambda: script_object.stop())
        stop_button.place(x=320, y=450, width=80, height=30)


if __name__ == "__main__":
    # 实例化脚本
    script = Script()

    # # 获取模拟器窗口句柄
    # script.get_hwnd()
    #
    # # 初始化模拟器窗口
    # script.init_mumu_window()

    main_thread = MyThread('主程序', script)
    main_thread.setDaemon(True)
    main_thread.start()

    # 注册助手
    tkinter = tk.Tk()
    app = App(tkinter, script)
    tkinter.mainloop()
