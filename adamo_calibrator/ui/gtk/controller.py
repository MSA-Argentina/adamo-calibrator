# -*- coding: utf-8 -*-
try:
    import gtk
except ImportError:
    print "You don't have GTK installed"
import pygtk
pygtk.require('2.0')

from gobject import source_remove, timeout_add
from pango import FontDescription

from adamo_calibrator.calibrator.calibrator import Calibrator
from adamo_calibrator.settings import DEBUG, FULLSCREEN, NPOINTS
from adamo_calibrator.ui.helpers import load_locales

INTERVAL = 50

load_locales()

# TODO:
# Implement auto_close
# Implement reset by errors.


class Window():

    def __init__(self, fake, device, misclick_threshold, dualclick_threshold,
                 finger_delta, timeout, fast_start, auto_close):
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

        self.calibrator = Calibrator(NPOINTS, misclick_threshold,
                                     dualclick_threshold, finger_delta, device,
                                     fake)

        screen = self.window.get_screen()
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.calibrator.set_screen_prop(self.width, self.height)

        if fast_start:
            self.status = ('calibrating', None)
            self.next = self.calibrator.get_next_point()
        else:
            self.status = ('init', None)
            self.next = (0, 0)
        self.counter = 0
        self.timeout = timeout
        if timeout != 0:
            self.timer = timeout_add(INTERVAL, self.timeout_quit)

        self.font = 'Helvetica 12'

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

    def timeout_quit(self):
        time_elapsed = self.counter / 1000
        if time_elapsed == 5:
            quit()
        else:
            drawable = self.drawable
            gc = self.gc
            self.counter += INTERVAL
            angle = (self.counter * 360) / self.timeout
            drawable.draw_arc(gc, True, self.width/2 - 25, self.height/2 + 25,
                              50, 50, 0, -angle*64)
            if self.next is not None:
                self.draw_pointer(self.next)
            return True

    def on_button_pressed(self, widget, event):
        if event.button == 1:
            # Reset Timeout
            self.counter = 0
            status = self.status[0]
            if status == 'init':
                self.status = ('calibrating', None)
                self.next = self.calibrator.get_next_point()
            elif status == 'calibrating' or status == 'error':
                data = (event.x_root, event.y_root)
                error = self.calibrator.add_click(data)
                if error is None:
                    msg = _("valid_click_detected")
                    if DEBUG:
                        print msg, data
                    self.next = self.calibrator.get_next_point()
                    self.status = ('calibrating', None)
                elif error == 'misclick':
                    msg = _("misclick_detected")
                    if DEBUG:
                        print msg, data
                    self.error(msg)
                elif error == 'doubleclick':
                    msg = _("doubleclick_detected")
                    if DEBUG:
                        print msg, data
                    self.error(msg)
            elif status == 'finish':
                quit()
        return True

    def on_button_released(self, widget, event):
        if event.button == 1:
            self.drawable.clear()
            if self.next is None:
                if self.timeout != 0:
                    source_remove(self.timer)
                self.finish()
            else:
                if self.status[0] == 'error':
                    self.error(self.status[1])
                else:
                    self.calibration_dialog()
                self.draw_pointer(self.next)
        return True

    def draw_text(self, width, height, font, text, rect=True, left=None,
                  top=None, text_top=None, text_left=None):
        drawing_area = self.drawing_area
        drawable = self.drawable
        gc = self.gc

        if left is None:
            left = self.width / 2 - width / 2
        if top is None:
            top = self.height / 2 - height / 2

        font_desc = FontDescription(font)

        layout = drawing_area.create_pango_layout(text)
        layout.set_font_description(font_desc)
        text_width, text_height = layout.get_pixel_size()

        if text_left is None:
            text_left = left + (width - text_width) / 2
        if text_top is None:
            text_top = top + (height - text_height) / 2
        if rect:
            drawable.draw_rectangle(gc, False, left, top, width, height)
            drawable.draw_rectangle(gc, False, left - 2, top - 2, width + 4,
                                    height + 4)
        drawable.draw_layout(gc, text_left, text_top, layout)

    def init_dialog(self, widget, event):
        font = 'Helvetica Bold 16'
        msg = _("title")
        self.draw_text(400, 200, font, msg, rect=False,
                       text_top=self.height/2 - 60)
        msg = _("init_msg")
        self.draw_text(400, 200, self.font, msg)
        if next is not None:
            self.draw_pointer(self.next)

    def calibration_dialog(self):
        msg = _("calibration_msg")
        self.draw_text(400, 200, self.font, msg)

    def end_dialog(self):
        self.status = ('finish', None)
        msg = _("finish_msg")
        self.draw_text(400, 200, self.font, msg)

    def error(self, msg):
        self.status = ('error', msg)
        self.draw_text(400, 200, self.font, msg)

    def finish(self):
        self.end_dialog()
        self.calibrator.calc_new_axis()
        self.calibrator.finish()
