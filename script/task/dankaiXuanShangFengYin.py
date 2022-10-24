import aircv

import app
import config
import logger
from script import pic, mouse, random


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
        yaoQing = pic.find("xuanshangfengyin.jpg", confidence=0.95, ux=624, uy=161, uw=194, uh=64)
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
