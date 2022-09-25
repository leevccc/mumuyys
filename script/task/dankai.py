import config
import logger
import script


def run():
    configs = config.Config()
    logger.info("单开养号")

    # 任务结束
    if configs.get("单开养号", "任务循环") != 1:
        script.run()
    else:
        script.random.sleep(configs.get("单开养号", "休息时间min"), configs.get("单开养号", "休息时间max"), "分")
