import config
import logger
import script
from script import window, fight, random


def run():
    logger.info("组队刷刷")
    if getConfig("模式") == "跟队模式":
        genDui()
    elif getConfig("模式") == "带队模式":
        daiDui()
    elif getConfig("模式") == "御魂挑战":
        yuHunTiaoZhan()


def genDui():
    times = getConfig("次数")
    script.setInfo("times", times)
    while times > 0:
        if getConfig("客户端数") > 1:
            window.switch(2)
        while fight.handleFightEnd() == "进行中":
            random.sleep()
        if getConfig("客户端数") >= 2:
            window.switch(3)
            while fight.handleFightEnd() == "进行中":
                random.sleep()
        if getConfig("客户端数") == 3:
            window.switch(4)
            while fight.handleFightEnd() == "进行中":
                random.sleep()
        times -= 1
        script.setInfo("times", times)


def daiDui():
    winDuiZhang = int(getConfig("队长窗口"))
    winMax = int(getConfig("客户端数"))
    # 切换到队长窗口
    window.switch(winDuiZhang + 1)

    times = getConfig("次数")
    script.setInfo("times", times)
    mode = "普通"
    while times > 0:
        # 队长挑战
        if mode == "普通" and fight.zuDuiTiaoZhan() is False:
            mode = "永生之海"
            logger.info("永生之海模式")
        if mode == "永生之海" and fight.zuDuiTiaoZhanYongShengZhiHai() is False:
            logger.info("找不到挑战按钮")
            mode = "普通"
            break
        # 处理第一个队员
        win = window.switchNext(winDuiZhang, winMax)
        while fight.handleFightEnd() == "进行中":
            random.sleep(msg="战斗进行中")
        # 处理第二个队员
        if getConfig("客户端数") >= 2:
            win = window.switchNext(win, winMax)
            while fight.handleFightEnd() == "进行中":
                random.sleep(msg="战斗进行中")
        # 处理第三个队员
        if getConfig("客户端数") == 3:
            window.switchNext(win, winMax)
            while fight.handleFightEnd() == "进行中":
                random.sleep(msg="战斗进行中")
        times -= 1
        script.setInfo("times", times)
        random.sleep(1, 2, "秒")


def yuHunTiaoZhan():
    times = getConfig("次数")
    script.setInfo("times", times)
    while times > 0:
        if fight.yuHunTiaoZhan() is False:
            logger.info("找不到挑战按钮")
            break
        while fight.handleFightEnd() == "进行中":
            random.sleep(1, 2, "秒")
        times -= 1
        script.setInfo("times", times)
        random.sleep(1, 2, "秒")


def getConfig(key):
    return config.Config().get("组队刷刷", key)
