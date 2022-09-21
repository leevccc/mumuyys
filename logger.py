import logging

module_logger = logging.getLogger(__name__)


class handlerLog(logging.StreamHandler):
    def __init__(self, app):
        logging.StreamHandler.__init__(self)
        self.app = app

    def emit(self, record):
        msg = self.format(record)
        self.app.log.config(state="normal")
        self.app.log.insert("end", msg + "\n")
        self.app.log.update()
        self.app.log.see("end")
        self.app.log.config(state="disabled")


def init(app):
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = handlerLog(app)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)
    module_logger.info("[日志信息]")
