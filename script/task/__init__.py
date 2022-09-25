from datetime import datetime

import config
import logger


def run(mode, name, taskFunc, daily=False):
    """
    运行任务
    :param mode: 单开模式/组队刷刷
    :param name: 任务名称
    :param taskFunc: 执行任务方法
    :param daily: 每天只做一次
    """
    configs = config.Config()
    enable = configs.get(mode, name)
    if enable == 1:
        if daily and configs.get("每日重置", "%s_%s" % (mode, name)) == "完成":
            logger.info("[任务] %s 今日已完成, 跳过" % name)
            return
        logger.info("[任务] %s" % name)
        result = taskFunc()
        if daily and result:
            # 每日任务完成标记
            configs.set("每日重置", "%s_%s" % (mode, name), "完成")


def setExecuteTime(taskName):
    configs = config.Config()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    configs.set("执行记录", taskName, now)


def isTimeExpired(taskName):
    configs = config.Config()
    result = False
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last = configs.get("执行记录", taskName)
    interval = configs.get("基本设置", taskName + "间隔")
    if last is None:
        result = True
    else:
        diff = datetime.strptime(now, "%Y-%m-%d %H:%M:%S") - datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        diff_hour = int(diff.seconds / 3600)
        if diff_hour > interval:
            result = True

    return result
