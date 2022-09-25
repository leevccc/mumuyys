import logger
import script
from script import pic, mouse
from script.task import tingyuan


def get():
    """
    获取当前位置
    :return: 当前位置
    """
    # 庭院
    result = "未知"
    if ZaiTingYuan() is True:
        result = "庭院"
    return result


def ZaiTingYuan():
    if script.getInfo("local") == "庭院":
        return True
    if pic.find("tansuo.jpg", times=2) is True:
        tingyuan.LingYuHun()
        tingyuan.LingShouSi()
        tingyuan.LingGouYu()
        return True
    return False


def QuTingYuan():
    close_button = [
        "close2.jpg"
    ]
    fanhui_button = [
        "fanhui.jpg",
        "fanhui2.jpg",
    ]

    while ZaiTingYuan() is False:
        logger.info("[动作] 返回庭院")
        for i in range(0, len(close_button)):
            if pic.click(close_button[i]):
                logger.info("[动作] 关闭界面")
        for i in range(0, len(fanhui_button)):
            if pic.click(fanhui_button[i], ux=0, uy=0, uw=100, uh=100) is True:
                logger.info("[动作] 返回上一级")
    script.setInfo("local", "庭院")


def QuYinYangLiao():
    logger.info("[位置] 打开阴阳寮界面")
    mouse.click(530, 674, 66, 73)
    script.setInfo("local", "阴阳寮")


def quJieJie():
    logger.info("[位置] 去结界")
    pic.click("jiejie.jpg", times=10)
    script.setInfo("local", "结界")
