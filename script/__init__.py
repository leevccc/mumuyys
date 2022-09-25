import ctypes
import time
from threading import Thread, current_thread

import config
import logger
from script import huodong, window, mouse, pic, random

user32 = ctypes.windll.user32  # 加载user32.dll
currentTask = -1
taskThread = []
currentInfo = []


class TaskThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        script()


def script():
    while True:
        if getRunning() == "运行中":
            configs = config.Config()
            moshi = configs.get("基本设置", "模式")
            if moshi == "活动模式":
                huodong.run()
        time.sleep(1)


def newThread():
    global taskThread, currentTask
    currentTask += 1
    # 初始化变量
    currentInfo.append({
        "running": "未开始",  # 未开始, 运行中, 暂停
        "local": "未知",
        "times": 0,
    })
    taskThread.append(TaskThread())
    taskThread[currentTask].daemon = True
    taskThread[currentTask].start()


def run():
    if getInfo("running") == "运行中":
        setInfo("running", "暂停")
        logger.info("暂停")
    else:
        setInfo("running", "运行中")
        logger.info("运行")
        window.initMuMuWindow()


def restart():
    if getRunning() == "未开始":
        return False
    # 暂停当前线程的任务
    setInfo("running", False)
    # 启用新线程
    newThread()
    logger.info("终止任务")


def getRunning():
    return getInfo("running")


def getInfo(key):
    return currentInfo[currentTask][key]


def setInfo(key, val):
    currentInfo[currentTask][key] = val
