import logger
import script.random
from script import pic, mouse, local, random


def QianDao():
    if pic.click("qiandao.jpg"):
        pic.click("qiandao2.jpg", times=30)
        script.random.sleep(1500, 2000)
        pic.click("close.jpg", times=10)
        return True
    return False


def HuangJinQianDao():
    if pic.click("huangjinqiandao.jpg"):
        script.random.sleep()
        mouse.click_100()
        return True
    return False


def ShangDianHeiDan():
    logger.info("[动作] 进入商店")
    # mouse.click(685, 684, 50, 60)
    if pic.click("shangdian.jpg") is False:
        return False
    script.setInfo("local", "商店")

    logger.info("[动作] 关闭推荐按钮")
    pic.click("close.jpg", times=4)

    logger.info("[动作] 进入礼包屋")
    mouse.click(1300, 714, 60, 60)

    logger.info("[动作] 点击黑蛋")
    mf = pic.click("mianfei.jpg", times=6)
    if mf is False:
        pic.click("tuijian.jpg")
        mf = pic.click("mianfei.jpg", times=6)
    if mf is False:
        logger.info("[!!!!!] 领取黑蛋失败")
    random.sleep(1000, 1500)
    mouse.click_100()
    local.quTingYuan()
    return True


def ShouYouQingDian():
    # mouse.click(964, 686, 62, 68)
    if pic.click("haoyou.jpg", times=4) is False:
        return False
    script.setInfo("local", "好友界面")
    if pic.click("youqingdian.jpg", times=4) is False:
        return False
    if pic.click("yijianlingqu.jpg", times=4) is False:
        return False
    random.sleep()
    mouse.click_100()
    local.quTingYuan()
    return True


def LingLiaoZiJin():
    local.quYinYangLiao()
    if pic.click("zijinlingqu.jpg", confidence=0.985, times=4):
        if pic.click("lingqu.jpg", times=4):
            random.sleep()
            mouse.click_100()
            return True
    return False
