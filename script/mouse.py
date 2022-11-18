import time

import pyautogui

import script
from script.task import dankaiXuanShangFengYin


def click(x, y, rw=0, rh=0, delay=True):
    """
    模拟鼠标点击

    :param x: 横坐标
    :param y: 纵坐标
    :param rw: 横坐标偏移范围
    :param rh: 纵坐标偏移范围
    :param delay: 是否需要延时
    """
    # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
    while script.getRunning() != "运行中":
        time.sleep(1)

    x += script.window.x
    y += script.window.y

    # 悬赏封印邀请处理
    dankaiXuanShangFengYin.handleHaoYouYaoQing()

    pyautogui.moveTo(x + script.random.get(t=rw), y + script.random.get(t=rh))
    if delay:
        script.random.sleep(msg="鼠标点击")
    pyautogui.click()


def click_100():
    click(120, 10, 80, 90)


def clickRightDown():
    click(1130, 616, 50, 50)


def clickThis(delay=True):
    if delay:
        script.random.sleep(msg="鼠标点击")
    pyautogui.click()
