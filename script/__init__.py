import ctypes
import inspect
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
    stop_thread(taskThread[currentTask - 1])


def getRunning():
    return getInfo("running")


def getInfo(key):
    return currentInfo[currentTask][key]


def setInfo(key, val):
    currentInfo[currentTask][key] = val


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
