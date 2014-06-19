from adamo_calibrator.ui.gtk.controller import Window


def run_gtk(fake=None, device=None, misclick_threshold=None,
            dualclick_threshold=None, finger_delta=None,
            timeout=None, fast_start=None, auto_close=None):
    window = Window(fake, device, misclick_threshold, dualclick_threshold,
                    finger_delta, timeout, fast_start, auto_close)

