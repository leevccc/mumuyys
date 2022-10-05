import logger
from script import task
from script.task import dankaiDaily, dankaiJieJie, dankaiTuPo


def run():
    logger.info("[模式] 单开养号")
    task.run("单开养号", "每日签到", dankaiDaily.QianDao, daily=True)
    task.run("单开养号", "黄金签到", dankaiDaily.HuangJinQianDao, daily=True)
    task.run("单开养号", "领取黑蛋", dankaiDaily.ShangDianHeiDan, daily=True)
    task.run("单开养号", "友情点", dankaiDaily.ShouYouQingDian, daily=True)
    task.run("单开养号", "领取寮资金", dankaiDaily.LingLiaoZiJin, daily=True)
    task.run("单开养号", "阴阳寮结界", dankaiJieJie.yinYangLiaoJieJie, daily=False)
    task.run("单开养号", "个人突破", dankaiTuPo.jieJieTuPo, daily=False)
    task.run("单开养号", "寮突破", dankaiTuPo.liaoTuPo, daily=False)

