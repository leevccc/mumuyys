import config
import logger
import script
from script import window, fight, random, pic, mouse


def run():
    logger.info("组队刷刷")
    if getConfig("模式") == "跟队模式":
        genDui()
    elif getConfig("模式") == "带队模式":
        daiDui()
    elif getConfig("模式") == "御魂挑战":
        yuHunTiaoZhan()
    elif getConfig("模式") == "跟队探索":
        genDuiTanSuo()


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


def genDuiTanSuo():
    logger.info("跟队探索")
    # 从探索战斗开始
    while True:
        if pic.find("tansuobox.jpg", ux=430, uy=283, uw=743, uh=372):
            logger.info("发现探索奖励箱子")
            pic.click("fanhui2.jpg", ux=0, uy=0, uw=120, uh=120)
            pic.click("tansuoqueren.jpg", times=4, ux=773, uy=422, uw=199, uh=69)
        elif pic.find("victory.jpg", confidence=0.98, ux=426, uy=58, uw=234, uh=211):
            logger.info("发现胜利状态 一")
            mouse.clickRightDown()
            while pic.find("victory2.jpg", confidence=0.90, ux=563, uy=442, uw=336, uh=284) is False:
                mouse.clickThis(delay=False)
                random.sleep(msg="等待胜利状态 二")
            while pic.find("victory2.jpg", confidence=0.90, ux=563, uy=442, uw=336, uh=284):
                mouse.clickThis(delay=False)
                random.sleep(msg="发现胜利状态 二")
        elif pic.find("failure.jpg", confidence=0.98, ux=426, uy=58, uw=234, uh=211):
            logger.info("发现失败状态")
            mouse.clickRightDown()
        elif pic.find("victory2.jpg", confidence=0.98, ux=563, uy=442, uw=336, uh=284):
            logger.info("发现胜利状态 二")
            mouse.clickRightDown()
            while pic.find("victory2.jpg", confidence=0.98, ux=563, uy=442, uw=336, uh=284):
                mouse.clickThis(delay=False)
                random.sleep(msg="发现胜利状态 二")
        elif pic.click("check.jpg", ux=106, uy=233, uw=99, uh=114):
            logger.info("发现邀请按钮")

        random.sleep()


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
