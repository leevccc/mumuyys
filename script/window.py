import win32con
import win32gui

import logger
import script

x, y, width, height = 0, 0, 1440, 810


def getHwnd():
    """
    获取 MuMu 窗口句柄
    """
    window = 0
    max_times = 3
    for i in range(0, max_times):
        window_title = "阴阳师 - MuMu模拟器"
        if i > 0:
            window_title = "#N" + str(i) + " 阴阳师 - MuMu模拟器"
        window = win32gui.FindWindow(0, window_title)
        if window != 0:
            break

    if window == 0:
        logger.info("找不到游戏窗口, 脚本退出")
        script.restart()
    return window


def initMuMuWindow():
    """
    调整模拟器位置和大小
    """
    global x, y
    hwnd = getHwnd()
    if hwnd == 0:
        return False
    # 还原窗口
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 激活窗口
    win32gui.SetForegroundWindow(hwnd)
    # 设置窗口位置和大小 宽 1440 高 899(含标题36 底部工具栏53) 实际分辨率 1440 x 810
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 1440, 899, win32con.SWP_SHOWWINDOW)
    # 获取窗口位置参数
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    x = left
    y = top + 36
    logger.info("窗口信息: 宽 " + str(right) + " 高 " + str(bottom) + " 顶 " + str(top) + " 左 " + str(
        left))
    logger.info("分辨率: 1440 x 810")
