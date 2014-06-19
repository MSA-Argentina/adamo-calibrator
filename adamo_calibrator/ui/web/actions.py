from zaguan.actions import BaseActionController
from adamo_calibrator.settings import DEBUG


class CalibratorControllerActions(BaseActionController):
    """Actions for calibrator controller"""

    def initiate(self, data):
        self.controller.initiate(data)

    def click(self, data):
        self.controller.register_click(data)

    def timeout(self, data):
        self.controller.quit(data)

    def log(self, data):
        """Action executed when 'log' is called and debug is True."""
        if DEBUG:
            print "LOG >>>", data
