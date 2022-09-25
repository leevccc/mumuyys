import time

import config
import logger
import script


def run():
    logger.info("活动模式")
    configs = config.Config()
    times = configs.get("活动模式", "次数")
    script.setInfo("times", times)
    while times > 0:
        logger.info("[动作] 战斗")
        script.pic.click("huodong\\fight.jpg")
        script.pic.find("ready.jpg", confidence=0.95, times=100)
        script.random.sleep(1500, 2000)
        logger.info("[动作] 准备")
        script.pic.click("ready.jpg", confidence=0.95, times=100)
        script.pic.click("huodong\\reward.jpg", confidence=0.95, times=1000)
        logger.info("[动作] 领取奖励")
        script.mouse.click(10, 10, 100, 100)
        script.random.sleep(1000, 1500)
        script.mouse.click(10, 10, 100, 100)
        script.random.sleep(1000, 1500)
        times -= 1
        script.setInfo("times", times)
        time.sleep(1)


def clickFightButton():
    logger.info("进入战斗")
