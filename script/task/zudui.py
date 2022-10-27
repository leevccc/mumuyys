import config
import logger
from script import window, fight, random


def run():
    logger.info("组队刷刷")
    if getConfig("跟队模式") == 1:
        genDui()


def genDui():
    while True:
        if getConfig("双开") == 1:
            window.switch(2)
        while fight.handleFightEnd() == "进行中":
            random.sleep(1, 2, "秒")
        if getConfig("双开") == 1:
            window.switch(3)
            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")
        random.sleep(6000, 7000)


def getConfig(key):
    return config.Config().get("组队刷刷", key)
