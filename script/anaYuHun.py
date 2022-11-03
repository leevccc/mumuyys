from datetime import datetime

import xlwings as xw

import app
import logger


def run():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wb = xw.Book(app.path + r"\yuhun.xlsx")
    data = wb.sheets["御魂方案"].range('A1').expand().value

    plan = ana(data)
    fPlan = formatPlan(plan)

    oldPlan = wb.sheets["强化方案"].range('A1').expand().value
    if oldPlan[0] == "方案":
        oldPlan = [["方案", "御魂", "生成时间"]]
    resultData = []
    for o in oldPlan:
        resultData.append(o)
    for f in fPlan:
        isNew = True
        for o in oldPlan:
            if f[0] == o[0] and f[1] == o[1]:
                isNew = False
            if isNew is False:
                break
        if isNew:
            f.append(now)
            resultData.append(f)

    wb.sheets["强化方案"].range('A1').expand().value = resultData
    wb.save()
    logger.info("输出完成")


def ana(data):
    yuhun = []
    plan = [
        {"名称": "头", "位置": [2], "御魂": ["全部"]},
        {"名称": "提速", "位置": [1, 3, 4, 5, 6], "御魂": ["全部"]},
        {"名称": "稀有暴爆", "位置": [6], "御魂": ["全部"]},
        {"名称": "因幡爆伤", "位置": ["全部"], "御魂": ["全部"]},
    ]
    # 整理御魂[[破势,2,攻,输出],[破势,4,攻,输出]]
    for item in data:
        if item[0] == "收录":
            continue  # 跳过标题行
        if item[2] is not None:
            yuhun.append([item[2], 2, item[4], item[8]])
            yuhun.append([item[2], 4, item[5], item[8]])
            yuhun.append([item[2], 6, item[6], item[8]])
        if item[3] is not None:
            yuhun.append([item[3], 2, item[4], item[8]])
            yuhun.append([item[3], 4, item[5], item[8]])
            yuhun.append([item[3], 6, item[6], item[8]])

    # 生成 246 号位方案
    for item in yuhun:
        # 过滤无属性
        if item[2] is None:
            continue
        # 过滤6号位稀有属性
        if item[2] in ["爆", "暴"]:
            continue
        name = "主%s副%s" % (item[2], item[3])
        # 过滤通用组合
        if name in ["主速副速"]:
            continue
        isNew = True
        for p in plan:
            if p["名称"] == name:
                isNew = False
                if item[1] not in p["位置"]:
                    p["位置"].append(item[1])
                    p["位置"].sort()
                if item[0] not in p["御魂"]:
                    p["御魂"].append(item[0])
        if isNew:
            plan.append({"名称": name, "位置": [item[1]], "御魂": [item[0]]})

    # 生成 135 号位方案
    for item in yuhun:
        # 过滤无指标
        if item[3] is None:
            continue
        # 过滤特殊指标
        if item[3] in ["速"]:
            continue
        name = item[3]
        isNew = True
        for p in plan:
            if p["名称"] == name:
                isNew = False
                if item[0] not in p["御魂"]:
                    p["御魂"].append(item[0])
        if isNew:
            plan.append({"名称": name, "位置": [1, 3, 5], "御魂": [item[0]]})

    return plan


def formatPlan(plan):
    result = []
    for p in plan:
        # 名称
        name = ""
        for n in p["位置"]:
            name += str(n)
        name += "-%s" % p["名称"]
        # 遍历御魂
        for y in p["御魂"]:
            result.append([name, y])
    return result
