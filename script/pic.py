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


def find(path, confidence=0.8, click=False, times=1, ux=None, uy=None, uw=None, uh=None, color=None, delay=0.0,
         double=False):
    """
    查找图片, 每隔 0.5 秒读取一次, 默认截图完整游戏窗口, 也可指定截图区域(ux, uy...)

    :param path: 图片相对地址
    :param confidence: 匹配度
    :param click: 识别后是否点击
    :param times: 次数
    :param ux: 游戏窗口的相对 x
    :param uy: 游戏窗口的相对 y
    :param uw: 截图宽度, 须配合ux
    :param uh: 截图高度, 须配合uy
    :param color: 格式 (255,255,255), 对找到的区域左上角进行颜色二次确认
    :param delay: 秒, 延迟后才点击
    :param double: True/False 是否双击
    :return: 按匹配结果依次返回: 失败 - None, None; 成功 - int(x), int(Y); 成功且需要点击 - True
    """
    # 脚本运行的本质是 识别图片+鼠标点击, 所以只需要在截图和点击功能里加入线程阻塞即可实现暂停功能
    while self.task_status is False:
        time.sleep(1)
    self.handle_xuan_shang_feng_yin()  # 图片识别前，先处理悬赏邀请
    match_result = None
    for i in range(0, times):
        self.print_screen(ux=ux, uy=uy, uwidth=uw, uheight=uh, file=path)
        screenshot = aircv.imread(self.path + "temp\\" + path.replace("\\", "_"))
        img = aircv.imread(self.path + path)

        match_result = aircv.find_template(screenshot, img, confidence)
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
        return False if click is True else (None, None)

    x, y = match_result["result"]

    if uh is not None:
        x += ux
        y += uy

    if click:
        x = match_result["rectangle"][0][0]
        y = match_result["rectangle"][0][1]
        width = match_result["rectangle"][3][0] - x
        height = match_result["rectangle"][3][1] - y
        if uh is not None:
            x += ux
            y += uy
        if color is not None and pyautogui.pixelMatchesColor(self.x + x, self.y + y, color) is False:
            return False

        if delay > 0:
            time.sleep(delay)
        self.click(x, y, width, height, double)
        return True

    if color is not None and pyautogui.pixelMatchesColor(self.x + x, self.y + y, color) is False:
        x, y = None, None

    return int(x), int(y)
