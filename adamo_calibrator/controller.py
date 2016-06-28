from __future__ import absolute_import
from __future__ import print_function

from random import randint
from sys import exit
from zaguan.actions import BaseActionController
from zaguan.controller import WebContainerController

from .calibrator import Calibrator
from .helpers import load_locales
from .settings import (
    NPOINTS, SHOW_CURSOR, DEBUG, RESOURCES_PATH, MISCLICK_THRESHOLD,
    DUALCLICK_THRESHOLD, TIMEOUT)


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


class CalibratorControllerActions(BaseActionController):
    """Actions for controller of Calibrator's UI"""

    def initiate(self, data):
        self.controller.initiate(data)

    def click(self, data):
        self.controller.register_click(data)

    def timeout(self, data):
        self.controller.quit(data)

    def log(self, data):
        """Action executed when 'log' is called and debug is True."""
        if DEBUG:
            print("LOG >>>", data)


class CalibratorController(WebContainerController):
    """ Controller of Calibrator's UI """

    def __init__(self, fake, device, fast_start, auto_close):
        """ Controller constructor
        """

        WebContainerController.__init__(self)
        instance = CalibratorControllerActions(controller=self)

        load_locales(RESOURCES_PATH)

        self.add_processor("calibrator", instance)

        self.calibrator = Calibrator(
            NPOINTS, MISCLICK_THRESHOLD, DUALCLICK_THRESHOLD, device, fake)

        self.fast_start = fast_start
        self.auto_close = auto_close
        self.state = None
        self.nerror = 0

    def initiate(self, data):
        """ Initialization of the calibration data with screen properties.
        """
        width = data[0]
        height = data[1]
        self.calibrator.set_screen_prop(width, height)
        print("Screen resolution: ", width, 'x', height)

        data = {}
        next = None
        self.state = 'init'
        if self.fast_start:
            self.state = 'calibrating'
            next = self.calibrator.get_next_point()

        self._calc_verification_point(width, height)

        data['show_cursor'] = SHOW_CURSOR
        data['timeout'] = TIMEOUT
        data['fast_start'] = self.fast_start
        data['auto_close'] = self.auto_close
        data['state'] = self.state
        data['next'] = next
        data['locale'] = get_base_data(TIMEOUT)
        data['verification_point'] = self.verification_point

        self.send_command('ready', data)

    def finish(self):
        """ End of calibration process
        """

        self.state = 'end'
        self.send_command('end')
        self.calibrator.finish()

    def reset(self):
        """ Reset calibration process
        """
        self.state = 'calibrating'
        self.nerror = 0
        self.calibrator.reset()

        width = self.calibrator.width
        height = self.calibrator.height
        self._calc_verification_point(width, height)
        self.send_command('reset', self.verification_point)

        next = self.calibrator.get_next_point()
        self.send_command('move_pointer', next)

    def _check_last_click(self, data):
        """ Checks the verification point to take the desition to restart the
            calibration.
        """

        (x, y) = data
        recalibrate = False
        misclick_threshold = 16
        if abs(self.verification_point[0] - x) > misclick_threshold or \
                abs(self.verification_point[1] - y) > misclick_threshold:
            recalibrate = True

        return recalibrate

    def _calc_verification_point(self, width, height):
        """ Calculates the position of the verification point
        """

        self.verification_point = (randint(width / 2 - 100, width / 2 + 100),
                                   randint(height / 2, height / 2 + 100))

    def register_click(self, data):
        """ Records the click's data sent by the frontend
        """

        state = self.state
        if state == 'init':
            self.state = 'calibrating'
            next = self.calibrator.get_next_point()
            self.send_command('move_pointer', next)
        elif state == 'calibrating':
            error = self.calibrator.add_click(data)
            if error is None:
                print(_("valid_click_detected"), data)
                next = self.calibrator.get_next_point()
                if next is None:
                    self.finish()
                else:
                    self.send_command('move_pointer', next)
            elif error == 'misclick':
                self.nerror += 1
                if self.nerror >= 3:
                    self.reset()
                print(_("misclick_detected"), data)
                self.send_command('error', error)
            elif error == 'doubleclick':
                self.nerror += 1
                if self.nerror >= 3:
                    self.reset()
                print(_("doubleclick_detected"), data)
                self.send_command('error', error)
        elif state == 'end':
            if self._check_last_click(data):
                print("Reset", data)
                self.reset()
            else:
                print("Close")
                self.quit(data)

    def quit(self, data):
        """ Exit function.
        """

        exit()
