from os.path import join, split

from gi.repository import Gtk, Gdk

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

from time import sleep
from zaguan import Zaguan
from adamo_calibrator.ui.web.controller import CalibratorController
from adamo_calibrator.settings import FULLSCREEN


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


def run_web(fake, device, misclick_threshold, dualclick_threshold,
            finger_delta, timeout, fast_start, auto_close, resources_path):
    controller = CalibratorController(fake, device, misclick_threshold,
                                      dualclick_threshold, finger_delta,
                                      timeout, fast_start, auto_close,
                                      resources_path)
    file_ = join(split(__file__)[0], 'web/html/index.html')
    uri = 'file://' + pathname2url(file_)
    zaguan = Window(uri, controller)
    zaguan.run()


if __name__ == "__main__":
    run_web()
