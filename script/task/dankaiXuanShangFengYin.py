import aircv
import pyautogui

import app
import config
import logger
from script import mouse, random, window


def handleHaoYouYaoQing(screenPrint=True, fileName=None):
    """
    处理悬赏封印邀请
    :param screenPrint: bool 是否需要截屏识别（pic中截屏识别请设置False，其他方法设置为True）
    :param fileName: string 不需要截屏时须提供temp目录下的图片名以供处理
    :return: bool 若识别到并处理了悬赏邀请则返回 True 否则为 False
    """
    result = False
    option = config.Config().get("基本设置", "悬赏邀请")
    if screenPrint:
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
        screen.save(app.tempImgPath + "xuanshangfengyin.jpg")

        screenshot = aircv.imread(app.tempImgPath + "xuanshangfengyin.jpg")
        imgObject = aircv.imread(app.imgPath + "\\" + "xuanshangfengyin.jpg")

        match_result = aircv.find_template(screenshot, imgObject, 0.95)
        yaoQing = match_result is not None
    else:
        screenshot = aircv.imread(app.tempImgPath + fileName)
        img = aircv.imread(app.imgPath + "xuanshangfengyin.jpg")
        match_result = aircv.find_template(screenshot, img, 0.95)
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

        mouse.click(rx, ry, rw, rh)
        random.sleep()
        result = True
    return result
