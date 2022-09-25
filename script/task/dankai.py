import config
import logger
import script
from script import task
from script.task import dankaiDaily


def run():
    configs = config.Config()
    logger.info("[模式] 单开养号")
    task.run("单开养号", "每日签到", dankaiDaily.QianDao, daily=True)
    task.run("单开养号", "黄金签到", dankaiDaily.HuangJinQianDao, daily=True)
    task.run("单开养号", "领取黑蛋", dankaiDaily.ShangDianHeiDan, daily=True)
    task.run("单开养号", "友情点", dankaiDaily.ShouYouQingDian, daily=True)
    task.run("单开养号", "领取寮资金", dankaiDaily.LingLiaoZiJin, daily=True)
    # 任务结束
    if configs.get("单开养号", "任务循环") != 1:
        script.run()
    else:
        script.random.sleep(configs.get("单开养号", "休息时间min"), configs.get("单开养号", "休息时间max"), "分")
