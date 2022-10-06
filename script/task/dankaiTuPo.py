import config
import logger
import script
from script import local, pic, random, mouse

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

    unlockZhenRong()

    running = True
    no = 1  # 挑战位置
    while running:
        # 判断是否完成
        if pic.find("gerentupowancheng.jpg", confidence=0.95, times=2, ux=1200, uy=0, uw=260, uh=70):
            running = False
            continue
        # 寻找未挑战的对象
        no = findObj(no=no, x=154, y=149, width=383, height=162)

        # 战斗
        logger.info("进攻第 %s 个结界" % no)
        x = 277 + (no - 1) % 3 * 374
        y = 196 + int((no - 1) / 3) * 152
        mouse.click(x, y, 220, 80)
        random.sleep()
        if attack() is False:
            logger.info("找不到进攻按钮, 请手动点击, 并按 F10 继续")
            script.run()
        ready()
        random.sleep(200, 500)
        switchAutoFight()
        random.sleep()
        greenMark()
        random.sleep(1, 3, "秒")

        result = handleFightEnd()
        while result == "进行中":
            random.sleep(1, 2, "秒")
            result = handleFightEnd()

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

    unlockZhenRong()

    running = True
    while running:
        if pic.find("liaotupowancheng.jpg", confidence=0.97) or pic.find("liaotupowancheng2.jpg", confidence=0.97):
            running = False
            continue

        # 寻找未挑战的对象
        no = findLiaoObj(x=465, y=147, width=379, height=151)
        if no == 0:
            running = False
            continue
        else:
            logger.info("进攻第 %s 个结界" % no)
            x = 581 + (no - 1) % 2 * 380
            y = 186 + int((no - 1) / 2) * 152
            mouse.click(x, y, 220, 70)
            random.sleep()
            if attack() is False or ready() is False:
                # 结界已被攻破无法进入战斗界面,先返回探索界面,重新进入寮界面
                # 下次切换进来要重新打开界面刷新数据, 否则多开可能同个寮, 其他窗口把你的目标突破了, 而你没刷新, 导致无法进攻
                mouse.click_100()
                local.quTanSuo()
                local.quLiaoTuPo()
                continue
            random.sleep(200, 500)
            switchAutoFight()
            random.sleep()
            greenMark()
            random.sleep(1, 3, "秒")

            while handleFightEnd() == "进行中":
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
    for no in range(1, 9):
        cx = x + (no - 1) % 2 * 380
        cy = y + int((no - 1) / 2) * 152
        status = yiTiaoZhan(cx, cy, width, height)
        if status == "未挑战":
            break
        elif no <= 8 and status == "已攻破":
            script.setInfo("寮突破今日目标", "已完成")
            return 0
        elif no == 8:
            return 0
    return no


def refreshList():
    logger.info("[动作] 刷新结界列表")
    pic.click("refresh.jpg")
    random.sleep(1000, 1500)
    pic.click("queding.jpg")
    random.sleep()


def yiTiaoZhan(x, y, width, height):
    if pic.find("po.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已攻破"
    if pic.find("po2.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已攻破"
    if pic.find("shibaibiaoji.jpg", ux=x, uy=y, uw=width, uh=height):
        return "已挑战"
    return "未挑战"


def attack():
    logger.info("点击进攻按钮")
    result = True
    if pic.click("attack.jpg", times=6) is False:
        logger.info("找不到进攻按钮")
        result = False
    return result


def ready():
    random.sleep(3, 4, "秒")
    if pic.click("ready.jpg", confidence=0.95, times=10) is True:
        logger.info("[动作] 准备")
        return True
    else:
        return False


def switchAutoFight():
    if pic.click("shoudong.jpg"):
        logger.info("[动作] 切换到自动战斗")


def greenMark():
    no = config.Config().get("单开养号", "突破绿标式神位")
    x, y, width, height = 0, 0, 45, 110
    if no == 0:
        return
    elif no == 1:
        x, y = 254, 522
    elif no == 2:
        x, y = 489, 452
    elif no == 3:
        x, y = 684, 427
    elif no == 4:
        x, y = 879, 452
    elif no == 5:
        x, y = 1129, 522

    # 点击范围缩小
    x += 5
    y += 5
    width -= 10
    height -= 10
    mouse.click(x, y, width, height)
    logger.info("[动作] 绿标 %s 号位式神" % no)


def handleFightEnd():
    result = "进行中"  # 转场动画, 如好友协战/刚结束战斗, 会导致无法找到返回按钮, 所以要设置一个默认值
    if pic.find("fanhui3.jpg", ux=0, uy=0, uw=100, uh=100):
        result = "进行中"  # 找到返回按钮, 则跳过后面的战斗结果检测
    elif pic.click("victory.jpg", confidence=0.98):
        random.sleep(500, 1000)
        pic.click("victory2.jpg", confidence=0.98, times=4)
        result = "胜利"
    elif pic.click("failure.jpg", confidence=0.98):
        result = "失败"
    elif pic.click("victory2.jpg", confidence=0.98):
        result = "胜利"

    if result != "进行中":
        logger.info("[状态] 战斗%s" % result)
    return result


def unlockZhenRong():
    if pic.click("suo.jpg") is True:
        logger.info("解除阵容锁")
