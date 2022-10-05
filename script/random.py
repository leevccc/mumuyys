import time
from random import random

import logger
import script


def get(f=0, t=100):
    """
    返回随机整数

    :param f: from 最小值
    :param t: to 最大值
    :return:
    """
    return f + round(random() * (t - f))


def sleep(f=500, t=1000, pType="毫秒"):
    """
    随机延迟 f ~ t 毫秒, 如果 f > t 则固定延迟 f

    :param f: from 最小毫秒
    :param t: to 最大毫秒
    :param pType: 参数类型 毫秒/秒/分/时
    """
    if f > t:
        t = f

    s = get(f, t)
    logger.info("[延时] %s %s" % (s, pType))

    # 把 s 转换为秒
    if pType == "毫秒":
        s /= 1000
    elif pType == "分":
        s = s * 60
    elif pType == "时":
        s = s * 3600

    script.setInfo("delay", s)
    sleeping()


def sleeping():
    while script.getInfo("delay") > 0:
        if script.getInfo("delay") > 1:
            time.sleep(1)
            script.setInfo("delay", script.getInfo("delay") - 1)
        else:
            time.sleep(script.getInfo("delay"))
            script.setInfo("delay", 0)
