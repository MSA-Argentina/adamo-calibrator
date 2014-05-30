from zaguan.actions import BaseActionController
from settings import DEBUG


class CalibratorControllerActions(BaseActionController):
    """Actions for calibrator controller"""

    def initiate(self, data):
        self.controller.set_resolution(data)

    def click(self, data):
        print "Click:", data
        self.controller.register_click(data)

    def log(self, data):
        """Action executed when 'log' is called and debug is True."""
        if DEBUG:
            print "LOG >>>", data
