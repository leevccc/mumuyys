from configparser import ConfigParser
import tkinter as tk
from datetime import datetime

import logger


class Config:
    conf = None  # 配置文件里的配置, 包含临时信息, 临时配置和界面配置
    configs = {}  # 可以在助手界面上修改的设置

    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read('config.ini')

    def init(self):
        configs = self.configs
        configs["基本设置"] = {}
        configs["基本设置"]["模式"] = tk.StringVar()
        configs["基本设置"]["模式"].set("单开养号")
        configs["基本设置"]["悬赏邀请"] = tk.StringVar()
        configs["基本设置"]["悬赏邀请"].set("取消")
        configs["单开养号"] = {}

        configs["单开养号"]["任务循环"] = tk.IntVar()
        configs["单开养号"]["任务循环"].set(1)
        configs["单开养号"]["休息时间min"] = tk.IntVar()
        configs["单开养号"]["休息时间min"].set(15)
        configs["单开养号"]["休息时间max"] = tk.IntVar()
        configs["单开养号"]["休息时间max"].set(30)

        configs["单开养号"]["庭院御魂"] = tk.IntVar()
        configs["单开养号"]["庭院御魂"].set(1)
        configs["单开养号"]["庭院寿司"] = tk.IntVar()
        configs["单开养号"]["庭院寿司"].set(1)
        configs["单开养号"]["庭院勾玉"] = tk.IntVar()
        configs["单开养号"]["庭院勾玉"].set(1)

        configs["单开养号"]["每日签到"] = tk.IntVar()
        configs["单开养号"]["每日签到"].set(1)
        configs["单开养号"]["黄金签到"] = tk.IntVar()
        configs["单开养号"]["黄金签到"].set(1)
        configs["单开养号"]["领取黑蛋"] = tk.IntVar()
        configs["单开养号"]["领取黑蛋"].set(1)
        configs["单开养号"]["友情点"] = tk.IntVar()
        configs["单开养号"]["友情点"].set(1)
        configs["单开养号"]["领取寮资金"] = tk.IntVar()
        configs["单开养号"]["领取寮资金"].set(1)

        configs["单开养号"]["阴阳寮结界"] = tk.IntVar()
        configs["单开养号"]["阴阳寮结界"].set(1)
        configs["单开养号"]["阴阳寮结界间隔"] = tk.IntVar()
        configs["单开养号"]["阴阳寮结界间隔"].set(1)
        configs["单开养号"]["结界卡"] = tk.StringVar()
        configs["单开养号"]["结界卡"].set("全部")
        configs["单开养号"]["结界卡排序"] = tk.StringVar()
        configs["单开养号"]["结界卡排序"].set("降序")

        configs["单开养号"]["个人突破"] = tk.IntVar()
        configs["单开养号"]["个人突破"].set(1)
        configs["单开养号"]["寮突破"] = tk.IntVar()
        configs["单开养号"]["寮突破"].set(1)
        configs["单开养号"]["突破绿标式神位"] = tk.IntVar()
        configs["单开养号"]["突破绿标式神位"].set(0)

        configs["单开养号"]["探索"] = tk.IntVar()
        configs["单开养号"]["探索"].set(1)
        configs["单开养号"]["探索次数"] = tk.IntVar()
        configs["单开养号"]["探索次数"].set(5)

        configs["单开养号"]["逢魔之时"] = tk.IntVar()
        configs["单开养号"]["逢魔之时"].set(1)

        configs["组队刷刷"] = {}
        configs["组队刷刷"]["模式"] = tk.StringVar()
        configs["组队刷刷"]["模式"].set("带队模式")
        configs["组队刷刷"]["客户端数"] = tk.IntVar()
        configs["组队刷刷"]["客户端数"].set(1)
        configs["组队刷刷"]["队长窗口"] = tk.IntVar()
        configs["组队刷刷"]["队长窗口"].set(1)
        configs["组队刷刷"]["次数"] = tk.IntVar()
        configs["组队刷刷"]["次数"].set(30)

        configs["活动模式"] = {}
        configs["活动模式"]["开启"] = tk.IntVar()
        configs["活动模式"]["开启"].set(1)
        configs["活动模式"]["次数"] = tk.IntVar()
        configs["活动模式"]["次数"].set(30)

        self.load()
        # 第一次运行的时候conf中没有任何值, 加载完再保存一遍确保conf中的值和内存中的值已同步
        self.save()
        # 清理完成记录
        self.clearDaily()

    def save(self):
        """
        保存脚本上的设置
        """
        configs = self.configs
        for _key in configs:
            if self.conf.has_section(_key) is False:
                self.conf.add_section(_key)
            for __key in configs[_key]:
                self.conf.set(_key, __key, str(configs[_key][__key].get()))
        self.conf.write(open('config.ini', 'w'))
        logger.info("保存配置")

    def load(self):
        """
        加载脚本设置
        """
        configs = self.configs
        for _key in configs:
            if self.conf.has_section(_key) is False:
                continue
            for __key in configs[_key]:
                if self.conf.has_option(_key, __key):
                    try:
                        configs[_key][__key].set(self.conf.getint(_key, __key))
                    except ValueError:
                        configs[_key][__key].set(self.conf.get(_key, __key))

    def set(self, section, key, val):
        """
        保存一个设置

        :param section: 设置组
        :param key: 设置名
        :param val: 设置值
        """
        conf = self.conf
        if conf.has_section(section) is False:
            conf.add_section(section)
        conf.set(section, key, val)
        conf.write(open('config.ini', 'w'))

    def get(self, section, key):
        """
        读取一个设置

        :param section: 设置组
        :param key: 设置名
        """
        conf = self.conf
        configs = self.configs
        result = None
        if conf.has_section(section) and conf.has_option(section, key):
            result = conf.get(section, key)
        # 如果是App上的设置则取App上的当前设置
        if section in configs and key in configs[section]:
            result = configs[section][key].get()
        return result

    def clearDaily(self):
        now = datetime.now()
        today = now.strftime("%Y%m%d")
        if self.conf.has_section("每日重置"):
            if self.conf.get("每日重置", "日期") != today:
                self.conf.remove_section("今日完成")
                self.set("每日重置", "日期", today)
        else:
            self.set("每日重置", "日期", today)
