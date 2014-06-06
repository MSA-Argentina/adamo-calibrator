from zaguan.controller import WebContainerController
from ui.web.actions import CalibratorControllerActions

from calibrator.calibrator import Calibrator
from settings import NPOINTS
from ui.helpers import load_locales
from ui.web.helpers import get_base_data

load_locales()


class CalibratorController(WebContainerController):

    def __init__(self, fake, device, misclick_threshold, dualclick_threshold,
                 finger_delta, timeout, fast_start):
        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)
        self.add_processor("calibrator", instance)

        self.calibrator = Calibrator(NPOINTS, misclick_threshold,
                                     dualclick_threshold, finger_delta, device,
                                     fake)

        self.timeout = timeout
        self.fast_start = fast_start
        self.state = None

    def initiate(self, data):
        self.calibrator.set_screen_prop(data[0], data[1])
        print "Screen resolution: ", data[0], 'x', data[1]

        data = {}
        next = None
        self.state = 'init'
        if self.fast_start:
            self.state = 'calibrating'
            next = self.calibrator.get_next_point()

        data['timeout'] = self.timeout
        data['fast_start'] = self.fast_start
        data['state'] = self.state
        data['next'] = next
        data['locale'] = get_base_data(self.timeout)

        self.send_command('ready', data)

    def finish(self):
        self.state = 'end'
        self.send_command('end')
        self.calibrator.calc_new_axis()
        self.calibrator.finish()

    def register_click(self, data):
        state = self.state
        if state == 'init':
            self.state = 'calibrating'
            next = self.calibrator.get_next_point()
            self.send_command('move_pointer', next)
        elif state == 'calibrating':
            error = self.calibrator.add_click(data)
            if error is None:
                print "Click valid: ", data
                next = self.calibrator.get_next_point()
                if next is None:
                    self.finish()
                else:
                    self.send_command('move_pointer', next)
            elif error == 'misclick':
                print "Error. Misclick detected: ", data
                self.send_command('error', error)
            elif error == 'doubleclick':
                print "Error. Doubleclick detected: ", data
                self.send_command('error', error)
        elif state == 'end':
            self.quit(data)

    def quit(self, data):
        quit()
