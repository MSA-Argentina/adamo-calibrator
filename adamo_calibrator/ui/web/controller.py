from zaguan.controller import WebContainerController
from adamo_calibrator.ui.web.actions import CalibratorControllerActions

from adamo_calibrator.calibrator.calibrator import Calibrator
from adamo_calibrator.settings import NPOINTS
from adamo_calibrator.ui.helpers import load_locales
#from adamo_calibrator.ui.web.helpers import get_base_data


def get_base_data(timeout):
    data = {'title': _('title'),
            'init_msg': _('init_msg'),
            'calibration_msg': _('calibration_msg'),
            'error_misclick': _('misclick_detected'),
            'error_doubleclick': _('doubleclick_detected'),
            'error_time': _('time_error'),
            'finish_msg': _('finish_msg')}

    if timeout != 0:
        max = timeout / 1000
        data['init_msg'] += _('wait').format(max)
        data['calibration_msg'] += _('wait').format(max)

    return data


class CalibratorController(WebContainerController):

    def __init__(self, fake, device, misclick_threshold, dualclick_threshold,
                 finger_delta, timeout, fast_start, auto_close,
                 resources_path):
        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)

        load_locales(resources_path)

        self.add_processor("calibrator", instance)

        self.calibrator = Calibrator(NPOINTS, misclick_threshold,
                                     dualclick_threshold, finger_delta, device,
                                     fake)

        self.timeout = timeout
        self.fast_start = fast_start
        self.auto_close = auto_close
        self.state = None
        self.nerror = 0

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
        data['auto_close'] = self.auto_close
        data['state'] = self.state
        data['next'] = next
        data['locale'] = get_base_data(self.timeout)

        self.send_command('ready', data)

    def finish(self):
        self.state = 'end'
        self.send_command('end')
        self.calibrator.calc_new_axis()
        self.calibrator.finish()

    def reset(self):
        self.nerror = 0
        self.calibrator.reset()
        next = self.calibrator.get_next_point()
        self.send_command('move_pointer', next)

    def register_click(self, data):
        state = self.state
        if state == 'init':
            self.state = 'calibrating'
            next = self.calibrator.get_next_point()
            self.send_command('move_pointer', next)
        elif state == 'calibrating':
            error = self.calibrator.add_click(data)
            if error is None:
                print _("valid_click_detected"), data
                next = self.calibrator.get_next_point()
                if next is None:
                    self.finish()
                else:
                    self.send_command('move_pointer', next)
            elif error == 'misclick':
                self.nerror += 1
                if self.nerror >= 3:
                    self.reset()
                print _("misclick_detected"), data
                self.send_command('error', error)
            elif error == 'doubleclick':
                self.nerror += 1
                if self.nerror >= 3:
                    self.reset()
                print _("doubleclick_detected"), data
                self.send_command('error', error)
        elif state == 'end':
            self.quit(data)

    def quit(self, data):
        quit()
