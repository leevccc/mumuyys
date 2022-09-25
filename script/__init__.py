import ctypes
import inspect
import time
from threading import Thread

import config
import logger
from script import window, mouse, pic, random, local
from script.task import huodong, dankai, zudui

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
    """
    脚本主循环
    """
    while True:
        if getRunning() == "运行中":
            configs = config.Config()
            moshi = configs.get("基本设置", "模式")

            # 初始化位置信息
            setInfo("local", local.get())
            if moshi == "单开养号":
                dankai.run()
            elif moshi == "组队刷刷":
                zudui.run()
            elif moshi == "活动模式":
                huodong.run()
        time.sleep(1)


def newThread():
    """
    创建任务线程, 并初始化临时信息
    """
    global taskThread, currentTask
    currentTask += 1
    # 初始化变量
    currentInfo.append({
        "running": "未开始",  # 未开始, 运行中, 暂停
        "local": "未知",
        "times": 0,
        "delay": 0,
    })
    taskThread.append(TaskThread())
    taskThread[currentTask].daemon = True
    taskThread[currentTask].start()


def run():
    """
    切换运行状态 - 运行中/暂停
    """
    if getInfo("running") == "运行中":
        setInfo("running", "暂停")
        logger.info("暂停")
    else:
        setInfo("running", "运行中")
        logger.info("运行")
        window.initMuMuWindow()


def restart():
    """
    创建新任务线程, 并结束旧任务线程, 仅任务运行中/暂停时可用
    """
    if getRunning() == "未开始":
        return False
    # 暂停当前线程的任务
    setInfo("running", False)
    # 启用新线程
    newThread()
    logger.info("终止任务")
    stop_thread(taskThread[currentTask - 1])


def getRunning():
    """
    获取任务运行状态
    """
    return getInfo("running")


def getInfo(key):
    """
    获取脚本参数
    :param key: 参数
    :return: 参数值
    """
    return currentInfo[currentTask][key]


def setInfo(key, val):
    """
    设置脚本参数值
    :param key: 参数
    :param val: 参数值
    """
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
