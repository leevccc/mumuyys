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

version = "v1.1.2"
module_logger = logging.getLogger(__name__)
user32 = ctypes.windll.user32  # 加载user32.dll


class Script:
    app = None
    log_tag = None
    task_status = False
    x = None
    y = None
    width = 1440
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

    def print_screen(self, ux=None, uy=None, uwidth=None, uheight=None):
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
        rx = self.x + self.width
        ry = self.y + self.height

        if uheight is not None:
            x += ux
            y += uy
            rx = x + uwidth
            ry = y + uheight

        # 截图前把鼠标移除出游戏界面
        mouse_x, mouse_y = pyautogui.position()
        if x < mouse_x < rx and y < mouse_y < ry:
            pyautogui.moveTo(rx, ry)

        screen = pyautogui.screenshot(region=(x, y, rx, ry))
        screen.save(self.path + "\\temp\\screenshot.jpg")

    def find_pic(self, path, confidence=0.8, click=False, times=1, ux=None, uy=None, uwidth=None, uheight=None):
        """
        查找图片, 每隔 0.5 秒读取一次, 默认截图完整游戏窗口, 也可指定截图区域(ux, uy...)

        :param path: 图片相对地址
        :param confidence: 匹配度
        :param click: 识别后是否点击
        :param times: 次数
        :param ux: 游戏窗口的相对 x
        :param uy: 游戏窗口的相对 y
        :param uwidth: 截图宽度, 须配合ux
        :param uheight: 截图高度, 须配合uy
        :return: 按匹配结果依次返回: 失败 - None, None; 成功 - int(x), int(Y); 成功且需要点击 - True
        """
        match_result = None
        for i in range(0, times):
            self.print_screen(ux=ux, uy=uy, uwidth=uwidth, uheight=uheight)
            screenshot = aircv.imread(self.path + "\\temp\\screenshot.jpg")
            img = aircv.imread(self.path + path)

            match_result = aircv.find_template(screenshot, img, confidence)
            # match_result
            # {
            #   'result': (1335.0, 731.5),
            #   'rectangle': ((1298, 682), (1298, 781), (1372, 682), (1372, 781)),
            #   'confidence': 0.993413507938385
            # }
            self.log("找图 [%s] - 结果: %s" % (path, match_result))
            if match_result is None:
                time.sleep(0.5)
                continue
            else:
                break

        if match_result is None:
            return False if click is True else (None, None)

        x, y = match_result["result"]

        if uheight is not None:
            x += ux
            y += uy

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
        self.click(120, 10, 80, 90)

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

    def is_time_expired(self, key):
        result = False
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last = self.app.get_daily_record(self.window, key + "执行")
        interval = self.app.settings["基本设置"][key + "间隔"].get()
        if last is None:
            result = True
        else:
            diff = datetime.strptime(now, "%Y-%m-%d %H:%M:%S") - datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
            diff_hour = int(diff.seconds / 3600)
            if diff_hour > interval:
                result = True

        return result

    def set_task_execute_time(self, key):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.set_daily_record(self.window, key + "执行", now)

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
        if self.find_pic("xinyoujian.jpg", confidence=0.99, click=True):
            self.log("[任务] 领取新邮件")
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
        self.action_open_yin_yang_liao()
        if self.find_pic("zijinlingqu.jpg", click=True, confidence=0.985, times=4):
            if self.find_pic("lingqu.jpg", click=True, times=4):
                self.random_sleep()
                self.click_100()
        self.action_hui_ting_yuan()

    def task_jie_jie(self):
        if self.is_time_expired("结界") is False:
            return
        if self.zt_zai_ting_yuan():
            self.action_open_yin_yang_liao()
        x, y = self.find_pic("xinxi2.jpg", times=4)
        if x is not None or self.find_pic("xinxi.jpg", click=True, times=4):
            self.action_open_jie_jie()
            if self.zt_zai_jie_jie():
                self.action_ling_qu_ti_li_shi_he()
                self.action_ling_qu_jing_yan_jiu_hu()
                self.action_ling_qu_ji_yang_exp()
                self.action_ling_qu_jie_jie_jiang_li()
                self.action_open_jie_jie_ka()
                if self.zt_jie_jie_ka_is_empty():
                    self.action_change_jie_jie_ka_sort()
                    self.action_change_jie_jie_ka_type()
                    self.action_use_jie_jie_ka()
                self.action_close_jie_jie_ka()
                if self.action_open_shi_shen_yu_cheng() is True:
                    self.action_change_full_shi_shen()
                    self.action_change_ji_yang()
                self.action_hui_ting_yuan()
            self.set_task_execute_time("结界")

    def action_open_yin_yang_liao(self):
        self.log("打开阴阳寮")
        self.click(530, 674, 66, 73)

    def action_open_jie_jie(self):
        self.log("打开结界")
        self.find_pic("jiejie.jpg", click=True)

    def action_ling_qu_ti_li_shi_he(self):
        if self.find_pic("tilishihe.jpg", click=True):
            self.log("领取体力食盒")
            self.find_pic("quchu.jpg", click=True, times=4)
            self.random_sleep()
            self.click_100()
            self.random_sleep()
            self.click_100()

    def action_ling_qu_jing_yan_jiu_hu(self):
        if self.find_pic("jingyanjiuhu.jpg", click=True):
            self.log("领取经验酒壶")
            self.find_pic("tiqu.jpg", click=True, times=4)
            self.random_sleep()

    def action_ling_qu_ji_yang_exp(self):
        if self.find_pic("jiyangjingyan.jpg", click=True):
            self.log("领取寄养经验")
            self.random_sleep()
            self.click_100()

    def action_ling_qu_jie_jie_jiang_li(self):
        self.log("领取结界卡奖励")
        self.click(1004, 169, 55, 55)
        self.random_sleep()

    def action_open_jie_jie_ka(self):
        self.log("打开结界卡界面")
        self.click(1000, 333, 40, 135)

    def action_change_jie_jie_ka_sort(self):
        sort = self.app.settings["window%s" % self.window]["星级"].get()
        pic = "xingjishengxu.jpg"
        if sort == "升序":
            pic = "xingjijiangxu.jpg"
        if self.find_pic(pic, click=True):
            self.log("调整星级排序为 %s" % sort)

    def action_change_jie_jie_ka_type(self):
        j_type = self.app.settings["window%s" % self.window]["结界卡"].get()
        if j_type == "全部":
            return

        self.log("更换结界卡类型")
        self.find_pic("quanbu.jpg", click=True)
        pic = ""
        if j_type == "太鼓":
            pic = "taigu.jpg"
        elif j_type == "斗鱼":
            pic = "douyu.jpg"
        elif j_type == "伞室内":
            pic = "sanshinei.jpg"
        elif j_type == "太阴符咒":
            pic = "taiyinfuzhou.jpg"
        elif j_type == "特殊变异":
            pic = "teshubianyi.jpg"

        self.find_pic(pic, click=True, times=2)

    def action_use_jie_jie_ka(self):
        self.log("激活结界卡")
        self.click(213, 206, 364, 109)
        self.random_sleep()
        self.find_pic("jihuo.jpg", click=True)
        self.random_sleep()
        self.find_pic("queding.jpg", click=True, times=4)
        self.random_sleep()

    def action_close_jie_jie_ka(self):
        self.log("关闭结界卡界面")
        self.click(1000, 333, 40, 135)
        self.find_pic("close2.jpg", click=True, times=4)
        self.random_sleep()

    def action_open_shi_shen_yu_cheng(self):
        self.log("打开式神育成")
        self.click(672, 350, 38, 112)
        x, y = self.find_pic("shishenyucheng.jpg", times=4)
        return x is not None

    def action_change_full_shi_shen(self):
        self.log("更换满级式神")
        count = 0
        while self.find_pic("man.jpg", click=True) is True:
            count += 1
        if count == 0:
            return
        self.random_sleep()
        self.find_pic("quanbu2.jpg", click=True)
        self.random_sleep()
        self.find_pic("sucai.jpg", click=True)
        self.random_sleep()
        for i in range(0, count):
            self.find_pic("baidan.jpg", confidence=0.95, click=True, ux=156, uy=551, uwidth=1107, uheight=237)
            self.random_sleep()

    def action_change_ji_yang(self):
        if self.find_pic("haoyoujiyang.jpg", click=True) is True:
            self.log("好友寄养")
            pics = ["6xtaigu.jpg", "6xdouyu.jpg", "5xtaigu.jpg", "5xdouyu.jpg", "4xtaigu.jpg", "4xdouyu.jpg"]
            for pic in pics:
                if self.find_pic(pic, confidence=0.95, click=True) is True:
                    break
            self.random_sleep()
            if self.find_pic("jinrujiejie.jpg", click=True) is True:
                x, y = self.find_pic("shishenyucheng.jpg", times=4)
                if x is not None:
                    self.random_sleep()
                    self.click(193, 590, 100, 118)
                    self.find_pic("queding.jpg", click=True, times=4)
                    # 候补式神再确定
                    self.find_pic("queding.jpg", click=True, times=4)

            self.action_hui_ting_yuan()

    def action_open_di_zang_xiang(self):
        self.click(1, 452, 35, 66)
        if self.find_pic("dizangxiang.jpg")[0] is not None:
            self.log("[动作] 打开地藏像")

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
            self.run_task("日常任务", "领取新邮件", self.task_mail)
            self.run_task("日常任务", "领取庭院寿司", self.action_ting_yuan_shou_si, False)
            self.run_task("日常任务", "领取庭院勾玉", self.action_ting_yuan_gou_yu, False)
            self.run_task("日常任务", "领取庭院御魂", self.action_ting_yuan_yu_hun, False)
            return True
        else:
            return False

    def zt_zai_jie_jie(self):
        x, y = self.find_pic("fanhui2.jpg", times=10)
        result = False
        if x is not None:
            self.log("[状态] 在结界")
            result = True
        return result

    def zt_jie_jie_ka_is_empty(self):
        x, y = self.find_pic("kongjiejieka.jpg", times=4)
        result = False
        if x is not None:
            self.log("[状态] 结界卡为空")
            result = True
        return result

    def task(self):
        while True:
            if self.task_status:
                times = self.clients
                while times > 0:
                    if self.zt_zai_ting_yuan():
                        self.action_kai_juan_zhou()
                        self.run_task("日常任务", "每日签到", self.task_qiandao, daily=True)
                        self.run_task("日常任务", "黄金签到", self.task_huang_jin_qiandao, daily=True)
                        self.run_task("日常任务", "领取黑蛋", self.task_shang_dian_fu_li, daily=True)
                        self.run_task("日常任务", "友情点", self.task_you_qing_dian, daily=True)
                        self.run_task("日常任务", "领取寮资金", self.task_liao_zi_jin, daily=True)
                        self.run_task("日常任务", "结界", self.task_jie_jie)

                    times -= 1
                    if 1 < self.clients and (self.window - 1) < self.clients:
                        # 最大客户端数大于 1 且当前窗口未超出客户端范围, 切换到下个窗口
                        self.switch_window()

                self.log("所有任务执行完毕")
                # 发出暂停命令
                self.run()
                # 设置需要初始化
                self.init = 0
                if self.app.settings["基本设置"]["任务循环"].get() == 1:
                    min_sleep_time = self.app.settings["基本设置"]["最小休息时间"].get()
                    max_sleep_time = self.app.settings["基本设置"]["最大休息时间"].get()
                    sleep_time = min_sleep_time + self.random_max(max_sleep_time - min_sleep_time)
                    self.syslog("休息 %s 分钟" % sleep_time)
                    time.sleep(sleep_time * 60)
                    # 发出运行命令 并进入新的循环
                    self.run()
            time.sleep(1)

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
    jie_jie_ka_options = ["全部", "太鼓", "斗鱼", "伞室内", "太阴符咒", "特殊变异"]
    settings_list = {
        "日常任务": {
            "常规任务": ["结界", ],
            "每日一次": [
                "每日签到",
                "黄金签到",
                "领取黑蛋",
                "友情点",
                "领取寮资金",
            ],
            "庭院发现": [
                "领取新邮件",
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
        root.title("mumu阴阳师助手 %s" % version)
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

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="日志信息")
        self.init_tab1(tab1)

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="基本设置")
        tab2.config(padding=10)
        self.init_tab2(tab2)

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="日常任务")
        tab3.config(padding=10)
        self.init_tab3(tab3)

        for i in range(2, 5):
            _tab = ttk.Frame(notebook)
            notebook.add(_tab, text="窗口%s" % i)
            _tab.config(padding=10)
            self.init_window_tab(_tab, "window%s" % i)

        # notebook.pack(expand=True, fill=tk.BOTH)
        notebook.place(x=0, y=0, width=self.width, height=430)

        # 底部按钮
        self.start_button_text = tk.StringVar()
        self.start_button_text.set("运行 F10")
        ttk.Button(root, textvariable=self.start_button_text, command=lambda: self.script_obj.run()) \
            .place(x=30, y=445, width=90, height=40)

        self.stop_button_text = tk.StringVar()
        self.stop_button_text.set("结束")
        ttk.Button(root, textvariable=self.stop_button_text, command=lambda: self.script_obj.kill("手动结束")) \
            .place(x=180, y=445, width=90, height=40)

        ttk.Button(root, text="保存配置", command=lambda: self.save_settings()) \
            .place(x=330, y=445, width=90, height=40)
        ttk.Button(root, text="读取配置", command=lambda: self.load_settings()) \
            .place(x=480, y=445, width=90, height=40)

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
            if self.conf.get("DailyRecord", "日期") != today:
                self.conf.remove_section("DailyRecord")
                self.set_conf("DailyRecord", "日期", today)
        else:
            self.set_conf("DailyRecord", "日期", today)

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
        self.settings["基本设置"]["任务循环"] = tk.IntVar()
        self.settings["基本设置"]["任务循环"].set(0)
        self.settings["基本设置"]["最小休息时间"] = tk.IntVar()
        self.settings["基本设置"]["最小休息时间"].set(15)
        self.settings["基本设置"]["最大休息时间"] = tk.IntVar()
        self.settings["基本设置"]["最大休息时间"].set(30)
        self.settings["基本设置"]["结界间隔"] = tk.IntVar()
        self.settings["基本设置"]["结界间隔"].set(1)
        self.settings["日常任务"] = {}
        for value in self.settings_list["日常任务"]["常规任务"]:
            self.settings["日常任务"][value] = tk.IntVar()
            self.settings["日常任务"][value].set(1)
        for value in self.settings_list["日常任务"]["每日一次"]:
            self.settings["日常任务"][value] = tk.IntVar()
            self.settings["日常任务"][value].set(1)
        for value in self.settings_list["日常任务"]['庭院发现']:
            self.settings["日常任务"][value] = tk.IntVar()
            self.settings["日常任务"][value].set(1)

        for i in range(2, 5):
            self.settings["window%s" % i] = {}
            self.settings["window%s" % i]["结界卡"] = tk.StringVar()
            self.settings["window%s" % i]["结界卡"].set("全部")
            self.settings["window%s" % i]["星级"] = tk.StringVar()
            self.settings["window%s" % i]["星级"].set("降序")

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

    # Tab: 基本设置
    def init_tab2(self, tab):
        ttk.Label(tab, text="客户端数", anchor='e').place(x=0, y=0, width=80, height=30)
        ttk.Radiobutton(tab, text="单开", value=1, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=90, y=0, width=60, height=30)
        ttk.Radiobutton(tab, text="双开", value=2, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=160, y=0, width=60, height=30)
        ttk.Radiobutton(tab, text="三开", value=3, variable=self.settings["基本设置"]["客户端数"]) \
            .place(x=230, y=0, width=60, height=30)

        ttk.Label(tab, text="任务循环", anchor="e").place(x=0, y=40, width=80, height=30)
        ttk.Radiobutton(tab, text="开启", value=1, variable=self.settings["基本设置"]["任务循环"]) \
            .place(x=90, y=40, width=60, height=30)
        ttk.Radiobutton(tab, text="禁用", value=0, variable=self.settings["基本设置"]["任务循环"]) \
            .place(x=160, y=40, width=60, height=30)
        ttk.Label(tab, text="休息时间(分钟)", anchor="e").place(x=220, y=40, width=110, height=30)
        ttk.Entry(tab, textvariable=self.settings["基本设置"]["最小休息时间"]) \
            .place(x=330, y=40, width=50, height=30)
        ttk.Label(tab, text="-", anchor="center").place(x=380, y=40, width=10, height=30)
        ttk.Entry(tab, textvariable=self.settings["基本设置"]["最大休息时间"]) \
            .place(x=390, y=40, width=50, height=30)

        ttk.Label(tab, text="结界任务间隔", anchor="e").place(x=0, y=80, width=80, height=30)
        ttk.Combobox(tab, textvariable=self.settings["基本设置"]["结界间隔"], values=["1", "2", "3", "4", "5", "6"],
                     state='readonly').place(x=90, y=80, width=60, height=30)
        ttk.Label(tab, text="小时", anchor="w").place(x=160, y=80, width=40, height=30)

    # 日常任务
    def init_tab3(self, tab):
        daily = ttk.LabelFrame(tab, text="每日一次", padding=10)
        daily.place(x=0, y=0, width=130, height=180)
        for i, val in enumerate(self.settings_list["日常任务"]['每日一次']):
            ttk.Checkbutton(daily,
                            text=val,
                            offvalue=0, onvalue=1,
                            variable=self.settings["日常任务"][val]) \
                .place(x=0, y=i * 30, width=110, height=20)

        common = ttk.LabelFrame(tab, text="常规任务", padding=10)
        common.place(x=140, y=0, width=130, height=180)
        for i, val in enumerate(self.settings_list["日常任务"]['常规任务']):
            ttk.Checkbutton(common,
                            text=val,
                            offvalue=0, onvalue=1,
                            variable=self.settings["日常任务"][val]) \
                .place(x=0, y=i * 30, width=110, height=20)

        ting_yuan = ttk.LabelFrame(tab, text="庭院发现", padding=10)
        ting_yuan.place(x=0, y=210, width=140, height=150)
        for i, val in enumerate(self.settings_list["日常任务"]['庭院发现']):
            ttk.Checkbutton(ting_yuan,
                            text=val,
                            offvalue=0, onvalue=1,
                            variable=self.settings["日常任务"][val]) \
                .place(x=0, y=i * 30, width=120, height=20)

    # 游戏窗口页面
    def init_window_tab(self, tab, window):
        ttk.Label(tab, text="结界卡", anchor="e").place(x=0, y=0, width=60, height=30)
        ttk.Combobox(tab, textvariable=self.settings[window]["结界卡"], values=self.jie_jie_ka_options,
                     state='readonly').place(x=65, y=0, width=110, height=30)
        ttk.Label(tab, text="星级").place(x=200, y=0, width=40, height=30)
        ttk.Radiobutton(tab, text="降序", value="降序", variable=self.settings[window]["星级"]) \
            .place(x=240, y=0, width=60, height=30)
        ttk.Radiobutton(tab, text="升序", value="升序", variable=self.settings[window]["星级"]) \
            .place(x=300, y=0, width=60, height=30)


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
