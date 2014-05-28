# -*- coding: utf-8 -*-
try:
    import gtk
except ImportError:
    print "You don't have GTK installed"

import pygtk
pygtk.require('2.0')
import pango

from calibrator.calibrator import Calibrator
from settings import DUALCLICK_THRESHOLD, FINGER_DELTA, MISCLICK_THRESHOLD, \
    NPOINTS, FULLSCREEN


class Window():

    def __init__(self):
        gtk.gdk.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)

        if FULLSCREEN:
            self.window.fullscreen()

        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.connect("expose_event", self.init_dialog)
        self.window.add(self.drawing_area)
        self.window.show_all()

        self.drawable = self.drawing_area.window
        self.gc = self.drawing_area.get_style().fg_gc[gtk.STATE_NORMAL]

        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK |
                               gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.EXPOSE)
        self.window.connect('button-press-event', self.on_button_pressed)
        self.window.connect('button-release-event', self.on_button_released)

        self.calibrator = Calibrator(NPOINTS, MISCLICK_THRESHOLD,
                                     DUALCLICK_THRESHOLD, FINGER_DELTA)

        screen = self.window.get_screen()
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.calibrator.set_screen_prop(self.width, self.height)

        self.status = (None, None)
        self.next = (0, 0)

        gtk.main()

    def draw_pointer(self, (centerx, centery)):
        drawable = self.drawable
        gc = self.gc

        size = 48

        x1 = centerx - size / 2
        x2 = centerx + size / 2
        y1 = centery - size / 2
        y2 = centery + size / 2
        r = 10

        drawable.draw_line(gc, centerx, y1, centerx, y2)
        drawable.draw_line(gc, x1, centery, x2, centery)
        drawable.draw_arc(gc, False, centerx-r/2, centery-r/2, r, r, 0, 360*64)

    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def on_button_pressed(self, widget, event):
        if event.button == 1 and self.status[0] is not 'init':
            data = (event.x_root, event.y_root)
            error = self.calibrator.add_click(data)
            if error is None:
                print "Click valid: ", data
                self.next = self.calibrator.get_next_point()
                self.status = ('calibrating', None)
            elif error == 'misclick':
                msg = "Misclick detected"
                print msg, ':', data
                self.error(msg)
            elif error == 'doubleclick':
                msg = "Doubleclick detected"
                print msg, ':', data
                self.error(msg)
            return True
        else:
            self.status = ('calibrating', None)
            self.next = self.calibrator.get_next_point()

    def on_button_released(self, widget, event):
        if event.button == 1:
            self.drawable.clear()
            if self.next is None:
                self.finish()
                quit()
            else:
                if self.status[0] == 'error':
                    self.error(self.status[1])
                self.draw_pointer(self.next)
        return True

    def init_dialog(self, widget, event):
        msg = "Please touch screen for start..."
        font = 'Helvetica 12'
        self.status = ('init', msg)
        self.draw_text(400, 200, font, msg)

    def draw_text(self, width, height, font, text):
        drawing_area = self.drawing_area
        drawable = self.drawable
        gc = self.gc

        left = self.width / 2 - width / 2
        top = self.height / 2 - height / 2

        font_desc = pango.FontDescription(font)

        layout = drawing_area.create_pango_layout(text)
        layout.set_font_description(font_desc)
        text_width, text_height = layout.get_pixel_size()

        text_left = left + (width - text_width) / 2
        text_top = top + (height - text_height) / 2
        drawable.draw_rectangle(gc, False, left, top, width, height)
        drawable.draw_rectangle(gc, False, left - 2, top - 2, width + 4, height + 4)
        drawable.draw_layout(gc, text_left, text_top, layout)

    def error(self, msg):
        self.status = ('error', msg)
        font = 'Helvetica 12'
        self.draw_text(200, 100, font, msg)

    def finish(self):
        self.calibrator.calc_new_axis()
        self.calibrator.finish()
