import time

import config
import logger
import script
from script import local, pic, mouse, fight, random


def run():
    times = config.Config().get("单开养号", "探索次数")
    script.setInfo("times", times)

    while times > 0:
        local.quTanSuoZhangJie()
        logger.info("点击探索按钮")
        pic.click("tansuoanniu.jpg", times=10)
        if pic.find("fanhui2.jpg", times=6) is False:
            logger.info("进入探索挑战失败")
            return False
        script.setInfo("local", "探索副本")

        finished = False
        rMove = False

        while finished is False:
            fighting = False
            if rMove:
                rightMove()
                rMove = False  # 重置变量

            if pic.click("tiaozhan.jpg", times=4, delay=False) \
                    and pic.find("fanhui3.jpg", times=10, ux=0, uy=0, uw=100, uh=100):
                logger.info("普通战斗")
                fighting = True
            elif pic.click("tiaozhanboss.jpg") and pic.find("fanhui3.jpg", times=10, ux=0, uy=0, uw=100, uh=100):
                logger.info("Boss战斗")
                fighting = True
                finished = True
            else:
                logger.info("未进入战斗")
                rMove = True

            if fighting:
                # 战斗处理
                while fight.handleFightEnd() == "进行中":
                    random.sleep(1, 2, "秒")
                random.sleep(1500, 2000)
        times -= 1
        script.setInfo("times", times)
        time.sleep(1)

    local.quTanSuoZhangJie()


def rightMove():
    logger.info("向右移动")
    mouse.click(1232, 589, 25, 25)
    random.sleep(2000, 2500)
