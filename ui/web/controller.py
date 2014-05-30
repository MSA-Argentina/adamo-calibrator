from zaguan.controller import WebContainerController
from ui.web.actions import CalibratorControllerActions

from calibrator.calibrator import Calibrator
from settings import NPOINTS


class CalibratorController(WebContainerController):

    def __init__(self, fake, device, misclick_threshold, dualclick_threshold,
                 finger_delta, timeout, fast_start):
        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)
        self.add_processor("calibrator", instance)

        self.calibrator = Calibrator(NPOINTS, misclick_threshold,
                                     dualclick_threshold, finger_delta, device,
                                     fake)

    def ready(self, data):
        next = self.calibrator.get_next_point()
        self.send_command('move_pointer', next)

    def set_resolution(self, data):
        self.calibrator.set_screen_prop(data[0], data[1])
        print "Screen resolution: ", data[0], 'x', data[1]
        self.send_command('ready')

    def finish(self):
        self.calibrator.calc_new_axis()
        self.calibrator.finish()

    def register_click(self, data):
        error = self.calibrator.add_click(data)
        if error is None:
            print "Click valid: ", data
            next = self.calibrator.get_next_point()
            if next is None:
                #TODO: Send finish message to frontend
                self.finish()
                quit()
            else:
                self.send_command('move_pointer', next)
        elif error == 'misclick':
            print "Misclick detected: ", data
            self.send_command('misclick', data)
        elif error == 'doubleclick':
            print "Doubleclick detected: ", data
            self.send_command('doubleclick', data)
