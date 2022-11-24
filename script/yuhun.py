import aircv
import cv2
import numpy as np
import pyautogui

import app
import logger
from script import window


def ana():
    # 识别几号位御魂
    screen = printScreen(643, 56, 368, 530)
    num = 0
    for i in range(1, 7):
        if getImg(str(i), screen) is not None:
            num = i
            break
    # 识别御魂名称
    yuHunList = {
        "bcf": "贝吹坊",
    }
    yuHun = None
    for k, v in yuHunList.items():
        if getImg(k, screen) is not None:
            yuHun = v
            break
    logger.info(f"{yuHun} {num}号位")

    # "清理图标"的坐标信息
    screen = printScreen()
    clean = getImg("clean", screen)
    # 只取左上角并转换为游戏里的相对坐标
    cleanX = clean["rectangle"][0][0] - window.x
    cleanY = clean["rectangle"][0][1] - window.y

    # 通过清理图标计算主属性位置
    mainX = cleanX - 231
    mainY = cleanY + 68

    # 主属性列表
    main = False
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
    # 识别主属性
    screen = printScreen(mainX, mainY, 150, 37)
    for k, v in mainList.items():
        if getImg(k, screen) is not None:
            main = v
            break
    logger.info("主属性 %s" % main)

    # 副属性列表
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
    # 遍历4个副属性词条
    fu = 0
    for i in range(1, 5):
        fuX = mainX
        fuY = mainY + i * 37
        screen = printScreen(fuX, fuY, 150, 37)
        # 识别副属性
        for k, v in fuList.items():
            if getImg(k, screen) is not None:
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


def getImg(fileName, screenshot, confidence=0.90):
    imgObject = cv2.imread(app.imgPath + "yuhun\\" + fileName + ".jpg")
    match = aircv.find_template(screenshot, imgObject, confidence)
    return match
