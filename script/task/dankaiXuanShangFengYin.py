import aircv
import cv2
import numpy as np
import pyautogui

import app
import config
import logger
from script import mouse, random, window


def handleHaoYouYaoQing():
    """
    处理悬赏封印邀请
    """
    result = False
    option = config.Config().get("基本设置", "悬赏邀请")
    x = window.x + 624
    y = window.y + 161
    w = 194
    h = 64
    rx = x + w
    ry = y + h

    # 截图前把鼠标移出截图区域
    mouse_x, mouse_y = pyautogui.position()
    if x < mouse_x < rx and y < mouse_y < ry:
        pyautogui.moveTo(rx + 1 + random.get(5, 10), ry + 1 + random.get(5, 10))

    screen = pyautogui.screenshot(region=(x, y, w, h))
    # screen.save(app.tempImgPath + "xuanshangfengyin.jpg")
    # screenshot = aircv.imread(app.tempImgPath + "xuanshangfengyin.jpg")
    screenshot = cv2.cvtColor(np.asarray(screen), cv2.COLOR_RGB2BGR)
    imgObject = aircv.imread(app.imgPath + "\\" + "xuanshangfengyin.jpg")
    match_result = aircv.find_template(screenshot, imgObject, 0.95)
    yaoQing = match_result is not None

    if yaoQing:
        rx, ry, rw, rh = 0, 0, 0, 0
        logger.info("悬赏封印自动 %s" % option)
        if option == "取消":
            rx, ry, rw, rh = 870, 129, 23, 25
        elif option == "接受":
            rx, ry, rw, rh = 935, 449, 50, 40
        elif option == "拒绝":
            rx, ry, rw, rh = 943, 565, 37, 39

        # mouse.click(rx, ry, rw, rh)
        pyautogui.moveTo(rx + window.x + random.get(t=rw), ry + window.y + random.get(t=rh))
        random.sleep(msg="鼠标点击")
        pyautogui.click()
        random.sleep()
        result = True
    return result
