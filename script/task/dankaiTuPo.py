import logger
import script
from script import local, pic, random, mouse, fight

success = 0
failure = 0


def init():
    global success, failure
    success = 0
    failure = 0


def setSuccess():
    global success
    success += 1


def setFailure():
    global failure
    failure += 1


def jieJieTuPo():
    init()
    while script.getInfo("local") != "结界突破":
        local.quJieJieTuPo()

    running = True
    no = 1  # 挑战位置
    while running:
        # 判断是否完成
        if pic.find("gerentupowancheng.jpg", confidence=0.98, times=2, ux=1200, uy=0, uw=260, uh=70):
            running = False
            continue
        # 寻找未挑战的对象
        no = findObj(no=no, x=154, y=149, width=383, height=162)

        # 战斗
        logger.info("进攻第 %s 个结界" % no)
        dx = (no - 1) % 3 * 374
        x = 277 + dx
        dy = int((no - 1) / 3) * 152
        y = 196 + dy
        mouse.click(x, y, 220, 80)
        random.sleep()
        if attack(343 + dx, 390 + dy, 185, 100) is False:
            continue
        random.sleep(4500, 5000)
        fight.greenMark()
        random.sleep(1, 3, "秒")

        result = fight.handleFightEnd()
        while result == "进行中":
            random.sleep(1, 2, "秒")
            result = fight.handleFightEnd()

        # 当前挑战后移
        no += 1
        # 胜利额外处理
        if result == "胜利":
            # 结界突破额外处理, 个人结界突破第 3,6,9 次攻破胜利会有额外奖励
            setSuccess()
            if success in [3, 6, 9]:
                logger.info("领取额外奖励")
                random.sleep(2000, 2500)
                pic.click("victory2.jpg", confidence=0.95)
        elif result == "失败":
            setFailure()
        random.sleep(1500, 2000)

    logger.info("[完成任务] 结界突破")


def liaoTuPo():
    if script.getInfo("寮突破今日目标") == "已完成":
        logger.info("寮突破今日目标已完成，跳过")
        return True
    if script.getInfo("local") != "寮突破":
        local.quLiaoTuPo()

    running = True
    while running:
        if pic.find("liaotupowancheng.jpg", confidence=0.98) or pic.find("liaotupowancheng2.jpg", confidence=0.98):
            running = False
            continue

        # 寻找未挑战的对象
        random.sleep(1000, 1500)
        no = findLiaoObj(x=465, y=147, width=379, height=151)
        if no == 0:
            running = False
            continue
        else:
            logger.info("进攻第 %s 个结界" % no)
            dx = (no - 1) % 2 * 380
            x = 581 + dx
            dy = int((no - 1) / 2) * 152
            y = 186 + dy
            mouse.click(x, y, 220, 70)
            random.sleep()
            if attack(659 + dx, 386 + dy, 167, 86) is False:
                # 结界已被攻破无法进入战斗界面,先返回探索界面,重新进入寮界面
                # 下次切换进来要重新打开界面刷新数据, 否则多开可能同个寮, 其他窗口把你的目标突破了, 而你没刷新, 导致无法进攻
                mouse.click_100()
                local.quTanSuo()
                local.quLiaoTuPo()
                continue
            random.sleep(4500, 5000)
            fight.greenMark()
            random.sleep(1, 3, "秒")

            while fight.handleFightEnd() == "进行中":
                random.sleep(1, 2, "秒")
            random.sleep(1000, 1500)

    logger.info("[完成任务] 寮突破")


def findObj(no, x, y, width, height):
    global failure
    if no > 9:  # 位置超标, 重置当前位置
        no = 1
        if failure > 0:
            refreshList()
        init()

    # 查找未挑战的结界
    while True:
        # 判断当前位置状态 未挑战/ 已挑战(失败)/ 已攻破
        cx = x + (no - 1) % 3 * 374
        cy = y + int((no - 1) / 3) * 152
        status = yiTiaoZhan(cx, cy, width, height)
        if status == "未挑战":
            break  # 结束查找
        elif status == "已挑战":
            setFailure()
        elif status == "已攻破":
            setSuccess()
        logger.info("第 %s 号位: %s" % (str(no), status))
        no += 1  # 当前位置无法挑战, 切换下一个位置
        if no > 9:  # 位置超标, 重置当前位置
            no = 1
            if failure > 0:
                refreshList()
            init()

    return no


def findLiaoObj(x, y, width, height):
    no = 1
    for no in range(1, 7):
        cx = x + (no - 1) % 2 * 380
        cy = y + int((no - 1) / 2) * 152
        status = yiTiaoZhan(cx, cy, width, height)
        if status == "未挑战":
            break
        elif no <= 6 and status == "已攻破":
            script.setInfo("寮突破今日目标", "已完成")
            return 0
        elif no == 6:
            return 0
    return no


def refreshList():
    logger.info("[动作] 刷新结界列表")
    pic.click("refresh.jpg")
    random.sleep(1000, 1500)
    pic.click("queding.jpg", ux=748, uy=441, uw=211, uh=90)
    random.sleep()


def yiTiaoZhan(x, y, width, height):
    if pic.find("po.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已攻破"
    if pic.find("po2.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已攻破"
    if pic.find("shibaibiaoji.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已挑战"
    return "未挑战"


def attack(ux, uy, uw, uh):
    logger.info("点击进攻按钮")
    result = True
    if pic.click("attack.jpg", times=6, ux=ux, uy=uy, uw=uw, uh=uh) is False:
        logger.info("找不到进攻按钮")
        result = False
    return result


def unlockZhenRong():
    if pic.click("suo.jpg") is True:
        logger.info("解除阵容锁")
