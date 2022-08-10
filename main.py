import os
import sys
import time
from random import random

import aircv
import pyautogui
# python -m pip install pypiwin32
# pip install pywin32
import win32con
import win32gui


class Script:
    # 初始化
    def __init__(self):
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
        x, y = match_result['result']

        return int(x), int(y)

    @staticmethod
    def click(x, y):
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
    def switch_window():
        pyautogui.hotkey('ctrl', '1')


if __name__ == '__main__':
    # 实例化脚本
    script = Script()
    script.get_hwnd()
    script.init_mumu_window()
    # script.click(760, 160)
    script.switch_window()
    # script.print_screen()
