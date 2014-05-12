import pygtk
pygtk.require('2.0')
import os
import urllib

from zaguan import Zaguan
from controller import CalibratorController


def load_window():
    controller = CalibratorController()
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_ = os.path.join(cur_dir, 'html/index.html')
    uri = 'file://' + urllib.pathname2url(file_)
    zaguan = Zaguan(uri, controller)
    zaguan.run()


if __name__ == "__main__":
    load_window()
