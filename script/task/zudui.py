import config
import logger
from script import window, fight, random


def run():
    logger.info("组队刷刷")
    if getConfig("模式") == "跟队模式":
        genDui()
    elif getConfig("模式") == "带队模式":
        daiDui()


def genDui():
    while True:
        if getConfig("客户端数") > 1:
            window.switch(2)
        while fight.handleFightEnd() == "进行中":
            random.sleep(1, 2, "秒")
        if getConfig("客户端数") >= 2:
            window.switch(3)
            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")
        if getConfig("客户端数") == 3:
            window.switch(4)
            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")
        random.sleep(6000, 7000)


def daiDui():
    winDuiZhang = int(getConfig("队长窗口"))
    winMax = int(getConfig("客户端数"))
    # 切换到队长窗口
    window.switch(winDuiZhang + 1)
    while True:
        # 队长挑战
        if fight.tiaoZhan() is False:
            logger.info("找不到挑战按钮")
            break
        # 处理第一个队员
        win = window.switchNext(winDuiZhang, winMax)
        while fight.handleFightEnd() == "进行中":
            random.sleep(1, 2, "秒")
        # 处理第二个队员
        if getConfig("客户端数") >= 2:
            win = window.switchNext(win, winMax)
            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")
        # 处理第三个队员
        if getConfig("客户端数") == 3:
            window.switchNext(win, winMax)
            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")


def getConfig(key):
    return config.Config().get("组队刷刷", key)
