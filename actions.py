from zaguan.actions import BaseActionController
from settings import DEBUG


class CalibratorControllerActions(BaseActionController):
    """Actions for calibrator controller"""

    def init(self, data):
        print data

    def document_ready(self):
        pass

    def initiate(self, data):
        print data

    def next_point(self):
        pass

    def click(self, data):
        print data

    def misclick_error(self):
        pass

    def duplicate_click_error(self):
        pass

    def log(self, data):
        """Action executed when 'log' is called and debug is True."""
        if DEBUG:
            print "LOG >>>", data
