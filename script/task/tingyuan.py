import config
import logger
import script.random
from script import pic, mouse

configs = config.Config()


def LingYuHun():
    if configs.get("单开养号", "庭院御魂") == 1 and pic.click("yuhun.jpg"):
        logger.info("[动作] 领取庭院御魂")
        pic.click("querenlingqu.jpg", times=4)
        script.random.sleep()
        mouse.click_100()


def LingShouSi():
    if configs.get("单开养号", "庭院寿司") == 1 and pic.click("shousi.jpg", confidence=0.95):
        logger.info("[动作] 领取庭院寿司")
        script.random.sleep()
        mouse.click_100()


def LingGouYu():
    if configs.get("单开养号", "庭院勾玉") == 1 and pic.click("gouyu.jpg"):
        logger.info("[动作] 领取庭院勾玉")
        script.random.sleep()
        mouse.click_100()
