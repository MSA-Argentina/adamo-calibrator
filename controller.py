from zaguan.controller import WebContainerController
from actions import CalibratorControllerActions


class CalibratorController(WebContainerController):

    def __init__(self):
        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)
        self.add_processor("calibrator", instance)

    def ready(self):
        pass
