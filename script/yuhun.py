import aircv
import cv2
import numpy as np
import pyautogui
import xlwings as xw
import app
import logger
from script import window

init = False
yuHunRowImgObject = {}
cleanImgObject = None
yuHunImgObject = {}
mainImgObject = {}
fuImgObject = {}

yuHunList = {
    "bcf": "贝吹坊",
    "bzb": "兵主部",
    "kg": "狂骨",
    "yml": "阴摩罗",
    "xy": "心眼",
    "mw": "鸣屋",
    "z": "狰",
    "lrd": "轮入道",
    "fy": "蝠翼",
    "hyhy": "海月火玉",
    "qnf": "青女房",
    "zn": "针女",
    "zms": "镇墓兽",
    "ps": "破势",
    "shn": "伤魂鸟",
    "wq": "网切",
    "sw": "三味",
    "el": "恶楼",
    "tf": "涂佛",
    "sy": "树妖",
    "zh": "薙魂",
    "zl": "钟灵",
    "jj": "镜姬",
    "bf": "被服",
    "npzh": "涅槃之火",
    "dzx": "地藏像",
    "csl": "出世螺",
    "my": "魅妖",
    "zz": "珍珠",
    "mm": "木魅",
    "rnss": "日女巳时",
    "fz": "反枕",
    "zcm": "招财猫",
    "xyh": "雪幽魂",
    "ynh": "遗念火",
    "fym": "飞缘魔",
    "bj": "蚌精",
    "hl": "火灵",
    "gq": "共潜",
    "ygx": "幽谷响",
    "fhx": "返魂香",
    "tzg": "骰子鬼",
    "wlzx": "魍魉之匣",
    "glgj": "鬼灵歌伎",
    "sql": "蜃气楼",
    "dzn": "地震鲶",
    "hkl": "荒骷髅",
    "lc": "胧车",
    "tzz": "土蜘蛛",
}
mainList = {
    "mGongJi": "攻击",
    "mFangYu": "防御",
    "mShengMing": "生命",
    "mSuDu": "速度",
    "mBaoJi": "暴击",
    "mBaoJiShangHai": "暴击伤害",
    "mGongJiJiaCheng": "攻击加成",
    "mFangYuJiaCheng": "防御加成",
    "mShengMingJiaCheng": "生命加成",
    "mXiaoGuoMingZhong": "效果命中",
    "mXiaoGuoDiKang": "效果抵抗",
}
fuList = {
    "fGongJi": "攻击",
    "fFangYu": "防御",
    "fShengMing": "生命",
    "fSuDu": "速度",
    "fBaoJi": "暴击",
    "fBaoJiShangHai": "暴击伤害",
    "fGongJiJiaCheng": "攻击加成",
    "fFangYuJiaCheng": "防御加成",
    "fShengMingJiaCheng": "生命加成",
    "fXiaoGuoMingZhong": "效果命中",
    "fXiaoGuoDiKang": "效果抵抗",
}

keyList = {
    "攻": "攻击加成",
    "防": "防御加成",
    "生": "生命加成",
    "速": "速度",
    "暴": "暴击",
    "爆": "暴击伤害",
    "命": "效果命中",
    "抵": "效果抵抗",
    "攻击加成": "攻击加成",
    "防御加成": "防御加成",
    "生命加成": "生命加成",
    "速度": "速度",
    "暴击": "暴击",
    "暴击伤害": "暴击伤害",
    "效果命中": "效果命中",
    "效果抵抗": "效果抵抗",
}

indexList = {
    "输出": "伤害输出",
    "命": "效果命中",
    "命中": "效果命中",
    "抵": "效果抵抗",
    "抵抗": "效果抵抗",
    "生": "生命加成",
    "攻": "攻击加成",
    "防": "防御加成",
    "速": "速度",
    "暴": "暴击",
    "爆": "暴击伤害",
    "治疗": "治疗量",
    "伤害输出": "伤害输出",
    "效果命中": "效果命中",
    "效果抵抗": "效果抵抗",
    "生命": "生命加成",
    "攻击": "攻击加成",
    "防御": "防御加成",
    "速度": "速度",
    "暴击": "暴击",
    "暴击伤害": "暴击伤害",
    "治疗量": "治疗量",
}


def initial():
    global init, cleanImgObject
    if init is False:
        logger.info("加载御魂位置素材")
        for i in range(1, 7):
            yuHunRowImgObject[str(i)] = getImgObjectByFileName(str(i))
        logger.info("加载御魂名称素材")
        for k, v in yuHunList.items():
            yuHunImgObject[k] = getImgObjectByFileName(f"\\type\\{k}")
        logger.info("加载清理图标素材")
        cleanImgObject = getImgObjectByFileName("clean")
        logger.info("加载主属性素材")
        for k, v in mainList.items():
            mainImgObject[k] = getImgObjectByFileName(k)
        logger.info("加载副属性素材")
        for k, v in fuList.items():
            fuImgObject[k] = getImgObjectByFileName(k)
        init = True


def readYuHun():
    initial()  # 初始化加载各种图片素材

    # 获取"清理图标"的坐标信息
    screen = printScreen()
    clean = findImgByImgObject(cleanImgObject, screen)
    # 只取左上角并转换为游戏里的相对坐标
    cleanX = clean["rectangle"][0][0]
    cleanY = clean["rectangle"][0][1]

    # 通过清理图标位置计算御魂名称和图标区域
    nameX = cleanX - 265
    nameY = cleanY - 70
    # 识别几号位御魂
    screen = printScreen(nameX, nameY, 253, 131)
    num = 0
    for k, v in yuHunRowImgObject.items():
        if findImgByImgObject(v, screen) is not None:
            num = k
            break
    # 识别御魂名称
    yuHunName = None
    for k, v in yuHunList.items():
        if findImgByImgObject(yuHunImgObject[k], screen) is not None:
            yuHunName = v
            break
    logger.info(f"{yuHunName} {num}号位")

    # 通过清理图标计算主属性位置
    mainX = cleanX - 231
    mainY = cleanY + 68

    # 主属性列表
    main = False
    # 识别主属性
    screen = printScreen(mainX, mainY, 150, 37)
    for k, v in mainList.items():
        if findImgByImgObject(mainImgObject[k], screen) is not None:
            main = v
            break
    logger.info("主属性 %s" % main)

    # 副属性列表
    # 遍历4个副属性词条
    fu = 0
    for i in range(1, 5):
        fuX = mainX
        fuY = mainY + i * 37
        screen = printScreen(fuX, fuY, 150, 37)
        # 识别副属性
        for k, v in fuList.items():
            if findImgByImgObject(fuImgObject[k], screen) is not None:
                logger.info("副属性%s %s" % (i, v))
                fu += 1
                break
    logger.info(f"共有副属性 {fu} 条")


def printScreen(ux=None, uy=None, uw=None, uh=None):
    x = window.x
    y = window.y
    w = x + window.width
    h = y + window.height
    if ux is not None:
        x += ux
        y += uy
        w = uw
        h = uh
    screen = pyautogui.screenshot(region=[x, y, w, h])
    # screen.save(app.tempImgPath + "test.jpg")
    screenshot = cv2.cvtColor(np.asarray(screen), cv2.COLOR_RGB2BGR)
    return screenshot


def findImgByFileName(fileName, screenshot, confidence=0.90):
    imgObject = cv2.imread(app.imgPath + "yuhun\\" + fileName + ".jpg")
    match = aircv.find_template(screenshot, imgObject, confidence)
    return match


def getImgObjectByFileName(fileName):
    return cv2.imread(app.imgPath + "yuhun\\" + fileName + ".jpg")


def findImgByImgObject(imgObject, screenshot, confidence=0.90):
    match = aircv.find_template(screenshot, imgObject, confidence)
    return match


def getPlan():
    excel = xw.Book(app.path + r"\yuhun.xlsx")
    data = excel.sheets["套装"].range('A1').expand().value
    planList = []
    packageList = []
    # 遍历全部套装
    num = 1
    for item in data:
        if item[0] == "使用场景":
            continue  # 跳过标题行
        package = {
            "编号": num,
            "使用场景": item[0],
            "式神": item[1],
            "御魂1": item[2],
            "御魂2": item[3],
            "二号位": keyList[item[4]],
            "四号位": keyList[item[5]],
            "六号位": keyList[item[6]],
            "指标1": indexList[item[7]],
            "指标2": None if item[8] is None else indexList[item[8]],
            "备注": item[9],
        }
        packageList.append(package)
        num += 1

        # 两个指标禁止相同或者同时为多属性指标
        if package["指标1"] == package["指标2"]:
            package["指标2"] = None
            logger.info("警告: 存在套装 指标1和指标2相同, 已无视指标2")

        # 指标决定副属性
        fuKeys = getFuKey(package["指标1"])
        fuKeys.extend(getFuKey(package["指标2"]))
        fuKeys = list(set(fuKeys))  # 去重
        fu = [None, None, None, None]
        i = 0
        for f in fuKeys:
            fu[i] = f
            i += 1

        planList.append(planData(package["御魂1"], 1, None, fu))
        planList.append(planData(package["御魂1"], 2, package["二号位"], fu))
        planList.append(planData(package["御魂1"], 3, None, fu))
        planList.append(planData(package["御魂1"], 4, package["四号位"], fu))
        planList.append(planData(package["御魂1"], 5, None, fu))
        planList.append(planData(package["御魂1"], 6, package["六号位"], fu))

        if package["御魂2"] is not None and package["御魂2"] != package["御魂1"]:
            planList.append(planData(package["御魂2"], 1, None, fu))
            planList.append(planData(package["御魂2"], 2, package["二号位"], fu))
            planList.append(planData(package["御魂2"], 3, None, fu))
            planList.append(planData(package["御魂2"], 4, package["四号位"], fu))
            planList.append(planData(package["御魂2"], 5, None, fu))
            planList.append(planData(package["御魂2"], 6, package["六号位"], fu))

    logger.info(packageList)
    logger.info(planList)


def getFuKey(index):
    if index is None:
        return []
    elif index == "治疗量":
        return ["生命加成", "暴击", "暴击伤害"]
    elif index == "伤害输出":
        return ["攻击加成", "暴击", "暴击伤害"]
    else:
        return [index]


def planData(yuHun, index, main=None, fu=None):
    if fu is None:
        fu = [None, None, None, None]

    if index == 1:
        m = "攻击"
    elif index == 3:
        m = "防御"
    elif index == 5:
        m = "生命"
    else:
        m = main

    return {
        "御魂": yuHun,
        "位置": index,
        "主属性": m,
        "副属性1": fu[0],
        "副属性2": fu[1],
        "副属性3": fu[2],
        "副属性4": fu[3],
    }


def ana():
    getPlan()
    # readYuHun()
