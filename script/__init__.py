import ctypes
import time
from threading import Thread

import config
import logger
from script import huodong, window

currentTask = -1
running = []  # 未开始, 运行中, 暂停
taskThread = []
user32 = ctypes.windll.user32  # 加载user32.dll


class TaskThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        script()


def script():
    while True:
        if running[currentTask]:
            configs = config.Config()
            moshi = configs.get("基本设置", "模式")
            if moshi == "活动模式":
                huodong.times = configs.get("活动模式", "次数")
                huodong.run()
        time.sleep(1)


def newThread():
    global taskThread, currentTask
    currentTask += 1
    running.append("未开始")
    taskThread.append(TaskThread())
    taskThread[currentTask].daemon = True
    taskThread[currentTask].start()


def run():
    if running[currentTask] == "运行中":
        running[currentTask] = "暂停"
        logger.info("暂停")
    else:
        running[currentTask] = "运行中"
        logger.info("运行")
        window.initMuMuWindow()


def restart():
    if getRunning() == "未开始":
        return False
    # 暂停当前线程的任务
    running[currentTask] = False
    # 启用新线程
    newThread()
    logger.info("终止任务")


def getRunning():
    return running[currentTask]
