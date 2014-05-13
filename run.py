try:
    import gtk
except ImportError:
    print  "You don't have GTK installed"

import pygtk
pygtk.require('2.0')
import os
import urllib

from time import sleep
from zaguan import Zaguan
from controller import CalibratorController
from settings import FULLSCREEN


class Window(Zaguan):

    def run_gtk(self, settings=None, window=None, debug=False):
        gtk.gdk.threads_init()

        if window is None:
            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
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
        gtk.main()


def load_window():
    controller = CalibratorController()
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_ = os.path.join(cur_dir, 'html/index.html')
    uri = 'file://' + urllib.pathname2url(file_)
    zaguan = Window(uri, controller)
    zaguan.run()


if __name__ == "__main__":
    load_window()
