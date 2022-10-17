import time

import aircv
import pyautogui

import app
import script
from script import window


def printScreen(ux=None, uy=None, uw=None, uh=None, uf="screenshot.jpg"):
    """
    游戏窗口截图，截图保存在 img/temp/ 目录下

    :param ux: 指定区域 x, 相对坐标 (仅游戏画面)
    :param uy: 指定区域 y, 相对坐标 (仅游戏画面)
    :param uw: 指定区域 宽度
    :param uh: 指定区域 高度
    :param uf: 指定保存的文件名
    """

    # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
    while script.getRunning() != "运行中":
        time.sleep(1)

    x = window.x
    y = window.y
    w = window.width
    h = window.height

    if uh is not None:
        x += ux
        y += uy
        w = uw
        h = uh

    rx = x + w
    ry = y + h

    # 截图前把鼠标移出截图区域
    mouse_x, mouse_y = pyautogui.position()
    if x < mouse_x < rx and y < mouse_y < ry:
        pyautogui.moveTo(rx, ry)

    screen = pyautogui.screenshot(region=(x, y, w, h))
    screen.save(app.tempImgPath + uf.replace("\\", "_"))


def get(img, confidence=0.9, times=1, ux=None, uy=None, uw=None, uh=None, details=False):
    """
    查找并获取图片的坐标, 返回游戏窗口的相对坐标, 且为目标的中心坐标

    :param img: img目录中的图片相对地址
    :param confidence: 匹配度 0~1
    :param times: 查找次数, 大于1次时, 每次间隔 0.5 秒
    :param ux: 游戏窗口的相对 x, 不指定则为整个游戏窗口
    :param uy: 游戏窗口的相对 y, 不指定则为整个游戏窗口
    :param uw: 截图宽度, 不指定则为整个游戏窗口
    :param uh: 截图高度, 不指定则为整个游戏窗口
    :param details: 是否返回坐标细节
    :return: False / x,y / details
    """
    # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
    while script.getRunning() != "运行中":
        time.sleep(1)

    match_result = None
    for i in range(0, times):
        printScreen(ux=ux, uy=uy, uw=uw, uh=uh, uf=img)
        screenshot = aircv.imread(app.tempImgPath + img.replace("\\", "_"))
        imgObject = aircv.imread(app.imgPath + "\\" + img)

        match_result = aircv.find_template(screenshot, imgObject, confidence)
        # match_result
        # {
        #   'result': (1335.0, 731.5),
        #   'rectangle': ((1298, 682), (1298, 781), (1372, 682), (1372, 781)),
        #   'confidence': 0.993413507938385
        # }
        # self.log("找图 [%s] - 结果: %s" % (path, match_result))
        if match_result is None and times > 1:
            time.sleep(0.5)
            continue
        else:
            break

    if match_result is None:
        return False
    if details is True:
        return match_result

    x, y = match_result["result"]

    if uh is not None:
        x += ux
        y += uy

    return [int(x), int(y)]


def find(img, confidence=0.9, times=1, ux=None, uy=None, uw=None, uh=None):
    """
    查找图片

    :param img: img目录中的图片相对地址
    :param confidence: 匹配度 0~1
    :param times: 查找次数, 大于1次时, 每次间隔 0.5 秒
    :param ux: 游戏窗口的相对 x, 不指定则为整个游戏窗口
    :param uy: 游戏窗口的相对 y, 不指定则为整个游戏窗口
    :param uw: 截图宽度, 不指定则为整个游戏窗口
    :param uh: 截图高度, 不指定则为整个游戏窗口
    :return: True/False
    """

    return False if get(img, confidence, times, ux, uy, uw, uh) is False else True


def click(img, confidence=0.9, times=1, ux=None, uy=None, uw=None, uh=None, delay=True):
    """
    查找并点击

    :param img: img目录中的图片相对地址
    :param confidence: 匹配度 0~1
    :param times: 查找次数, 大于1次时, 每次间隔 0.5 秒
    :param ux: 游戏窗口的相对 x, 不指定则为整个游戏窗口
    :param uy: 游戏窗口的相对 y, 不指定则为整个游戏窗口
    :param uw: 截图宽度, 不指定则为整个游戏窗口
    :param uh: 截图高度, 不指定则为整个游戏窗口
    :param delay: 是否需要延时
    :return: True/False
    """
    details = get(img, confidence, times, ux, uy, uw, uh, True)
    if details is False:
        return False

    x = details["rectangle"][0][0]
    y = details["rectangle"][0][1]
    width = details["rectangle"][3][0] - x
    height = details["rectangle"][3][1] - y
    if uh is not None:
        x += ux
        y += uy

    script.mouse.click(x, y, width, height, delay)
    return True
