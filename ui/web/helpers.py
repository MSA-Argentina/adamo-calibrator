# -*- coding: utf-8 -*-

from ui.helpers import load_locales

load_locales()


def get_base_data():
    data = {'title': _('title'),
            'init_msg': _('init_msg'),
            'calibration_msg': _('calibration_msg'),
            'error_misclick': _('misclick_detected'),
            'error_doubleclick': _('doubleclick_detected'),
            'error_time': _('time_error'),
            'finish_msg': _('finish_msg')}
    return data
