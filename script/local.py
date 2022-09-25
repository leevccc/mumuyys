import script
from script import pic


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
        return True
    return False
