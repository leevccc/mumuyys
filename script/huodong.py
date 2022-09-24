import logger

times = 0


def run():
    global times
    while times > 0:
        times -= 1


def clickFightButton():
    logger.info("进入战斗")
