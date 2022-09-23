import time
from threading import Thread

import logger

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
        logger.info("运行")
    else:
        logger.info("暂停")


def script():
    while True:
        if running:
            logger.info("run")
        time.sleep(1)

