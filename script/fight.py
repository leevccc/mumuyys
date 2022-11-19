import config
import logger
from script import random, pic, mouse


def ready():
    random.sleep(3, 4, "秒")
    if pic.click("ready.jpg", confidence=0.95, times=10, ux=1231, uy=576, uw=200, uh=190) is True:
        logger.info("[动作] 准备")
        return True
    else:
        return False


def switchAutoFight():
    if pic.click("shoudong.jpg"):
        logger.info("[动作] 切换到自动战斗")


def zuDuiTiaoZhan():
    if pic.click("zuduitiaozhan.jpg", times=4, ux=1266, uy=614, uw=214, uh=196):
        logger.info("[动作] 组队挑战")
        return True
    return False


def zuDuiTiaoZhanYongShengZhiHai():
    if pic.click("zuduitiaozhanyongshengzhihai.jpg", times=4, ux=1266, uy=614, uw=214, uh=196):
        logger.info("[动作] 挑战永生之海")
        return True
    return False


def yuHunTiaoZhan():
    mouse.click(1267, 691, 69, 57)
    return True


def greenMark():
    no = config.Config().get("单开养号", "突破绿标式神位")
    x, y, width, height = 0, 0, 45, 50
    if no == 0:
        return
    elif no == 1:
        x, y = 254, 522
    elif no == 2:
        x, y = 489, 452
    elif no == 3:
        x, y = 684, 410
    elif no == 4:
        x, y = 879, 452
    elif no == 5:
        x, y = 1129, 522

    mouse.click(x, y, width, height)
    logger.info("[动作] 绿标 %s 号位式神" % no)


def handleFightEnd():
    result = "进行中"  # 转场动画, 如好友协战/刚结束战斗, 会导致无法找到返回按钮, 所以要设置一个默认值
    if pic.find("fanhui3.jpg", ux=0, uy=0, uw=100, uh=100):
        result = "进行中"  # 找到返回按钮, 则跳过后面的战斗结果检测
    elif pic.find("victory.jpg", confidence=0.98, ux=426, uy=58, uw=234, uh=211):
        logger.info("识别到胜利状态 一")
        mouse.clickRightDown()
        while pic.find("victory2.jpg", confidence=0.90, ux=563, uy=442, uw=336, uh=284) is False:
            mouse.clickThis(delay=False)
            random.sleep(msg="等待胜利状态 二")
        while pic.find("victory2.jpg", confidence=0.90, ux=563, uy=442, uw=336, uh=284):
            logger.info("识别到胜利状态 二")
            mouse.clickThis()
        result = "胜利"
    elif pic.find("failure.jpg", confidence=0.98, ux=426, uy=58, uw=234, uh=211):
        logger.info("识别到失败状态")
        random.sleep()
        mouse.clickRightDown()
        result = "失败"
    elif pic.find("victory2.jpg", confidence=0.98, ux=563, uy=442, uw=336, uh=284):
        logger.info("识别到胜利状态 二")
        mouse.clickRightDown()
        while pic.find("victory2.jpg", confidence=0.98, ux=563, uy=442, uw=336, uh=284):
            logger.info("识别到胜利状态 二")
            mouse.clickThis()
        result = "胜利"

    if result != "进行中":
        logger.info("[状态] 战斗%s" % result)
    return result
