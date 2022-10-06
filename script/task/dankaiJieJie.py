import config
import logger
import script.local
from script import task, local, pic, random, mouse


def yinYangLiaoJieJie():
    if task.isTimeExpired("阴阳寮结界") is False:
        logger.info("时间间隔不足， 跳过")
        return
    if script.getInfo("local") != "阴阳寮" and local.zaiTingYuan() is False:
        local.quTingYuan()
        local.quYinYangLiao()

    if pic.find("xinxi2.jpg", times=4) or pic.click("xinxi.jpg", times=4):
        local.quJieJie()
        lingQuTiLiShiHe()
        lingQuJingYanJiuHu()
        lingQuJieJieKaJiangLi()
        lingQuJiYangJingYan()
        daKaiJieJieKa()
        if jieJieKaWeiKong():
            gengGaiJieJieKaPaiXu()
            gengGaiJieJieKaZhongLei()
            shiYongJieJieKa()
        guanBiJieJieKa()
        if daKaiShiShenYuCheng() is True:
            gengHuanManJiShiShen()
            haoYouJiYang()
        task.setExecuteTime("阴阳寮结界")
        local.quTingYuan()


def lingQuTiLiShiHe():
    if pic.click("tilishihe.jpg"):
        logger.info("[动作] 领取体力食盒")
        pic.click("quchu.jpg", times=4)
        random.sleep()
        mouse.click_100()
        random.sleep()
        pic.click("close2.jpg")


def lingQuJingYanJiuHu():
    if pic.click("jingyanjiuhu.jpg"):
        logger.info("[动作] 领取经验酒壶")
        pic.click("tiqu.jpg", times=4)
        random.sleep()
        pic.click("close2.jpg")
    elif pic.click("jingyanjiuhu2.jpg"):
        logger.info("[动作] 领取经验酒壶")
        pic.click("tiqu.jpg", times=4)
        random.sleep()
        pic.click("close2.jpg")


def lingQuJiYangJingYan():
    if pic.click("jiyangjingyan.jpg"):
        logger.info("[动作] 领取寄养经验")
        random.sleep()
        mouse.click_100()


def lingQuJieJieKaJiangLi():
    logger.info("[动作] 领取结界卡奖励")
    mouse.click(1004, 169, 55, 55)
    random.sleep()


def daKaiJieJieKa():
    logger.info("[动作] 打开结界卡界面")
    mouse.click(1000, 333, 40, 135)


def jieJieKaWeiKong():
    xy = pic.find("kongjiejieka.jpg", times=4)
    result = False
    if xy:
        logger.info("结界卡为空")
        result = True
    return result


def gengGaiJieJieKaPaiXu():
    sort = config.Config().get("单开养号", "结界卡排序")
    img = "xingjishengxu.jpg"
    if sort == "升序":
        img = "xingjijiangxu.jpg"
    if pic.click(img):
        logger.info("[动作] 调整星级排序为 %s" % sort)


def gengGaiJieJieKaZhongLei():
    j_type = config.Config().get("单开养号", "结界卡")
    if j_type == "全部":
        return

    logger.info("[动作] 更换结界卡类型")
    pic.click("quanbu.jpg")
    img = ""
    if j_type == "太鼓":
        img = "taigu.jpg"
    elif j_type == "斗鱼":
        img = "douyu.jpg"
    elif j_type == "伞室内":
        img = "sanshinei.jpg"
    elif j_type == "太阴符咒":
        img = "taiyinfuzhou.jpg"
    elif j_type == "特殊变异":
        img = "teshubianyi.jpg"

    pic.click(img, times=2)


def shiYongJieJieKa():
    logger.info("[动作] 激活结界卡")
    mouse.click(213, 206, 364, 109)
    random.sleep()
    pic.click("jihuo.jpg")
    random.sleep()
    pic.click("queding.jpg", times=4)
    random.sleep()


def guanBiJieJieKa():
    logger.info("[动作] 关闭结界卡界面")
    pic.click("close2.jpg", times=4)
    random.sleep()


def daKaiShiShenYuCheng():
    logger.info("[动作] 打开式神育成")
    mouse.click(672, 350, 38, 112)
    xy = pic.find("shishenyucheng.jpg", times=4)
    return xy is not False


def gengHuanManJiShiShen():
    logger.info("[动作] 更换满级式神")
    count = 0
    while pic.click("man.jpg") is True:
        count += 1
    if count == 0:
        return
    random.sleep()
    pic.click("quanbu2.jpg")
    random.sleep()
    pic.click("sucai.jpg")
    random.sleep()
    for i in range(0, count):
        pic.click("baidan.jpg", confidence=0.98, ux=156, uy=551, uw=1107, uh=237)
        random.sleep()
        # 候补式神再确定
        pic.click("queding.jpg", times=4, ux=469, uy=271, uw=492, uh=260)


def haoYouJiYang():
    if pic.click("haoyoujiyang.jpg") is True:
        random.sleep(1000, 1500)
        logger.info("[动作] 好友寄养")
        pics = ["6xtaigu.jpg", "6xdouyu.jpg", "5xtaigu.jpg", "5xdouyu.jpg", "4xtaigu.jpg", "4xdouyu.jpg"]
        for img in pics:
            if pic.click(img, confidence=0.95) is True:
                break
        random.sleep()
        if pic.click("jinrujiejie.jpg") is True:
            xy = pic.find("shishenyucheng.jpg", times=4)
            if xy:
                random.sleep()
                mouse.click(193, 590, 100, 118)
                pic.click("queding.jpg", times=4)
                # 候补式神再确定
                random.sleep()
                pic.click("queding.jpg", times=4, ux=469, uy=271, uw=492, uh=260)

        local.quTingYuan()
