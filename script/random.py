import time
from random import random


def get(f=0, t=100):
    """
    返回随机整数

    :param f: from 最小值
    :param t: to 最大值
    :return:
    """
    return f + round(random() * (t - f))


def sleep(f=500, t=1000):
    """
    随机延迟 f ~ t 毫秒, 如果 f > t 则重设 t = f + 500

    :param f: from 最小毫秒
    :param t: to 最大毫秒
    """
    if f > t:
        t = f + 500

    sleep = get(f, t)
    time.sleep(sleep / 1000)
