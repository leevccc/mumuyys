import logger
from script import task, local, pic


def yinYangLiaoJieJie():
    if task.isTimeExpired("阴阳寮结界") is False:
        logger.info("时间间隔不足， 跳过")
        return
    if local.ZaiTingYuan() is False:
        local.QuTingYuan()
    local.QuYinYangLiao()

    xy = pic.get("xinxi2.jpg", times=4)
    if xy is not False or pic.click("xinxi.jpg", times=4):
        local.quJieJie()
        self.action_ling_qu_ti_li_shi_he()
        self.action_ling_qu_jing_yan_jiu_hu()
        self.action_ling_qu_jie_jie_jiang_li()
        self.action_ling_qu_ji_yang_exp()
        self.action_open_jie_jie_ka()
        if self.zt_jie_jie_ka_is_empty():
            self.action_change_jie_jie_ka_sort()
            self.action_change_jie_jie_ka_type()
            self.action_use_jie_jie_ka()
        self.action_close_jie_jie_ka()
        if self.action_open_shi_shen_yu_cheng() is True:
            self.action_change_full_shi_shen()
            self.action_change_ji_yang()
        task.setExecuteTime("阴阳寮结界")
    local.QuYinYangLiao()
