import logger
import script
from script import pic, mouse, random
from script.task import tingyuan


def get():
    """
    获取当前位置
    :return: 当前位置
    """
    # 庭院
    result = "未知"
    if zaiTingYuan() is True:
        result = "庭院"
    return result


def zaiTingYuan():
    if script.getInfo("local") == "庭院":
        return True
    if pic.find("tansuo.jpg", times=2) is True:
        tingyuan.lingYuHun()
        tingyuan.lingShouSi()
        tingyuan.lingGouYu()
        return True
    return False


def quTingYuan():
    close_button = [
        "close2.jpg"
    ]
    fanhui_button = [
        "fanhui.jpg",
        "fanhui2.jpg",
    ]

    while zaiTingYuan() is False:
        logger.info("[动作] 返回庭院")
        for i in range(0, len(close_button)):
            if pic.click(close_button[i]):
                logger.info("[动作] 关闭界面")
        for i in range(0, len(fanhui_button)):
            if pic.click(fanhui_button[i], ux=0, uy=0, uw=100, uh=100) is True:
                logger.info("[动作] 返回上一级")
    script.setInfo("local", "庭院")


def quYinYangLiao():
    logger.info("[位置] 打开阴阳寮界面")
    # mouse.click(530, 674, 66, 73)
    if pic.click("liao.jpg") is False:
        return False
    script.setInfo("local", "阴阳寮")
    return True


def quJieJie():
    logger.info("[位置] 去结界")
    pic.click("jiejie.jpg", times=10)
    pic.find("fanhui2.jpg", times=10)
    script.setInfo("local", "结界")


def zaiTanSuo():
    result = False

    if script.getInfo("local") == "探索":
        result = True

    if result is False:
        result = pic.find("yao.jpg", times=4)

    if result is True:
        script.setInfo("local", "探索")

    return result


def quTanSuo():
    while script.getInfo("local") != "探索":
        logger.info("[位置] 进入探索界面")
        # 庭院打开路线
        if script.getInfo("local") == "庭院":
            pic.click("tansuo.jpg")
        # 突破界面打开路线
        if script.getInfo("local") in ["结界突破", "寮突破"]:
            pic.click("close2.jpg")
        # 打开失败, 回庭院
        if zaiTanSuo() is False:
            quTingYuan()


def quTanSuoZhangJie():
    zaiTanSuo()  # 探索副本没奖励会直接跳出到探索界面，需重置位置

    while script.getInfo("local") != "探索章节":
        if script.getInfo("local") == "探索副本":
            logger.info("返回探索界面")
            pic.click("fanhui2.jpg", times=2)
            pic.click("tansuoqueren.jpg", times=2)
            if zaiTanSuo() is False:  # 打完出年兽会自动跳回到探索界面
                script.setInfo("local", "探索章节")
        else:
            logger.info("[位置] 打开探索章节")
            quTanSuo()
            logger.info("打开第二十八章")
            if pic.click("tansuo\\28.jpg", times=4):
                script.setInfo("local", "探索章节")


def zaiJieJieTuPo():
    result = False

    if script.getInfo("local") == "结界突破":
        result = True

    if result is False:
        result = pic.find("fangshoujilu.jpg", times=6)

    if result is True:
        script.setInfo("local", "结界突破")

    return result


def quJieJieTuPo():
    while script.getInfo("local") != "结界突破":
        logger.info("[位置] 打开结界突破界面")
        # 庭院打开路线
        if script.getInfo("local") == "庭院":
            quTanSuo()
        if script.getInfo("local") == "探索":
            pic.click("jiejietupo.jpg", times=10)
        # 寮突破打开路线
        if script.getInfo("local") == "寮突破":
            pic.click("geren.jpg", times=10)
        # 打开失败, 回庭院
        if zaiJieJieTuPo() is False:
            quTingYuan()
    script.setInfo("local", "结界突破")


def zaiLiaoTuPo():
    result = False

    if script.getInfo("local") == "寮突破":
        result = True

    if result is False:
        result = pic.find("tupojilu.jpg", times=6)

    if result is True:
        script.setInfo("local", "寮突破")

    return result


def quLiaoTuPo():
    while script.getInfo("local") != "寮突破":
        logger.info("[位置] 切换寮突破界面")
        # 庭院打开路线
        if script.getInfo("local") == "庭院":
            quTanSuo()
        if script.getInfo("local") == "探索":
            quJieJieTuPo()
        if script.getInfo("local") == "结界突破":
            pic.click("yinyangliao.jpg", times=10)
        # 打开失败, 回庭院
        if zaiLiaoTuPo() is False:
            quTingYuan()
    script.setInfo("local", "寮突破")
