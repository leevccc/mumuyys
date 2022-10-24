import os
from datetime import datetime

import app
import logger
import script
from script import local, pic, random, mouse, fight


def run():
    now = datetime.now()
    h = int(now.strftime("%H"))
    m = int(now.strftime("%M"))
    if h < 17:
        logger.info("还没到 17 点，跳过")
        return False
    if h == 21 and m >= 45:
        logger.info("为了留足时间，超过 21：45 脚本不再执行逢魔之时任务，跳过")
        return False
    if h > 22:
        logger.info("已经超过 22 点，跳过")
        return False

    # 回到庭院
    local.quTingYuan()
    # 点击地藏像
    pic.click("dizang.jpg")
    pic.click("richang.jpg", times=4)
    pic.click("fengmozhishi.jpg", times=4)
    pic.click("qianwang.jpg", times=4)
    pic.find("fanhui2.jpg", times=10)
    script.setInfo("local", "逢魔之时")

    # 现世逢魔
    while pic.find("hun.jpg"):
        mouse.click(1310, 715, 55, 55)
        random.sleep(5, 7, "秒")

    # 领取逢魔奖励
    mouse.click(1371, 246, 39, 38)
    random.sleep(1000, 1500)
    mouse.click_100()

    # 4个位置处理
    handleEvent(1340, 309, 85, 77)
    handleEvent(1365, 389, 75, 70)
    handleEvent(1332, 454, 96, 84)
    handleEvent(1354, 540, 86, 67)

    # 首领挑战
    boss()
    local.quTingYuan()
    return True


def handleEvent(x, y, uw, uh):
    if pic.find("fengmofeng.jpg", ux=x, uy=y, uw=uw, uh=uh):
        logger.info("已完成，跳过")
    elif pic.click("fengmomixin.jpg", ux=x, uy=y, uw=uw, uh=uh):
        qa()
    elif pic.click("fengmoyao.jpg", ux=x, uy=y, uw=uw, uh=uh):
        yao()

    random.sleep()


def boss():
    logger.info("逢魔 Boss")
    pic.click("fengmoshouling.jpg", times=4)
    pic.click("fengmoshouling2.jpg", times=10)
    pic.click("jijietiaozhan.jpg", times=4)
    pic.click("queding.jpg", times=4)
    if pic.find("fengmoshishenlu.jpg", times=6):
        script.setInfo("local", "逢魔Boss")
        pic.click("ready.jpg", times=600)
        random.sleep(3, 3, "分")
        pic.find("fengmoshishenlu.jpg", times=600)
        mouse.click(30, 19, 27, 34)
        pic.click("quereng.jpg", times=4)


def box():
    logger.info("逢魔宝箱")


def qa():
    logger.info("逢魔密信")
    folder = app.imgPath + "fengmoqa\\"
    files = int(len(os.listdir(folder)) / 2)
    logger.info("题库数量 %s" % files)
    while pic.find("fengmomixin2.jpg"):
        finished = False
        i = 0
        while finished is False:
            i += 1
            if pic.find("q%s.jpg" % i, ux=477, uy=145, uw=513, uh=133):
                pic.click("q%sa.jpg" % i, ux=477, uy=284, uw=504, uh=290)
                random.sleep(1500, 2000)
                mouse.click_100()
                finished = True
            if i == files and finished is False:
                logger.info("题库中找不到题目，请手动补充题库，并按 F10 恢复脚本，让脚本完成自动答题")
                script.run()
                random.sleep(24, 72, "时")


def yao():
    logger.info("逢魔妖怪")
    fight.ready()
    fight.handleFightEnd()
    random.sleep()
