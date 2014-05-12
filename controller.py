from zaguan.controller import WebContainerController
from actions import CalibratorControllerActions

from calibrator import Calibrator


class CalibratorController(WebContainerController):

    def __init__(self):
        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)
        self.add_processor("calibrator", instance)

        self.calibrator = Calibrator(5, 30, 15)

    def ready(self, data):
        next = self.calibrator.get_next_point()
        self.send_command('move_pointer', next)

    def set_resolution(self, data):
        self.calibrator.set_screen_prop(data[0], data[1])
        self.send_command('ready')

    def finish(self):
        self.calibrator.calc_new_axis(0, 2047, 0, 2047)
        self.calibrator.finish()

    def register_click(self, data):
        error = self.calibrator.add_click(data)
        if error is None:
            next = self.calibrator.get_next_point()
            if next is None:
                #TODO: Send finish message to frontend
                print self.calibrator.clicks
                self.finish()
                quit()
            else:
                self.send_command('move_pointer', next)
