import time
from threading import Thread

import config
import logger
from script import huodong, window

running = False


class TaskThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        script()


def run():
    global running
    running = running is False
    if running:
        window.initMuMuWindow()
        logger.info("运行")
    else:
        logger.info("暂停")


def script():
    while True:
        if running:
            configs = config.Config()
            moshi = configs.get("基本设置", "模式")
            if moshi == "活动模式":
                huodong.times = configs.get("活动模式", "次数")
                huodong.run()
        time.sleep(1)
