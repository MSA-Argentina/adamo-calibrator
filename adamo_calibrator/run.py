#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

from argparse import ArgumentParser
from os.path import join, split
from time import sleep

from gi.repository import Gtk, Gdk
from zaguan import Zaguan

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

from .controller import CalibratorController
from .settings import FULLSCREEN, FAST_START, AUTO_CLOSE


class Window(Zaguan):
    def run_gtk(self, settings=None, window=None, debug=False):
        Gdk.threads_init()

        if window is None:
            self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
            self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        else:
            self.window = window

        browser = self.controller.get_browser(self.uri, debug=debug,
                                              settings=settings)
        self.window.set_border_width(0)
        self.window.add(browser)

        sleep(1)
        self.window.show_all()
        self.window.show()
        if FULLSCREEN:
            self.window.fullscreen()
        Gtk.main()


def run(fake, device, fast_start, auto_close):
    controller = CalibratorController(fake, device, fast_start, auto_close)
    file_ = join(split(__file__)[0], 'resources/index.html')
    uri = 'file://' + pathname2url(file_)
    zaguan = Window(uri, controller)
    zaguan.run()


def main():
    parser = ArgumentParser()
    group_dev = parser.add_mutually_exclusive_group()

    group_dev.add_argument('--device', type=int, metavar='dev-id',
                           default=None,
                           help='Set device ID manually for calibration.')
    group_dev.add_argument('--fake', action="store_true",
                           help="Use a fake device.")
    parser.add_argument('--faststart', action="store_true", default=FAST_START,
                        help="Start calibrating.")
    parser.add_argument('--autoclose', action="store_true", default=AUTO_CLOSE,
                        help="Close without user click.")
    parser.add_argument('-l', '--list', action="store_true",
                        help='List calibratables devices available.')
    args = parser.parse_args()

    if args.list:
        from adamo_calibrator.export.xinput import XInput
        devices = XInput.get_device_with_prop('Evdev Axis Calibration',
                                              id_only=False)
        print("Devices:")
        for name, id, setted in devices:
            print(("\tId: {0:2}\tName: {1}".format(id, name)))

    run(fake=args.fake, device=args.device, fast_start=args.faststart,
        auto_close=args.autoclose)


if __name__ == "__main__":
    main()
