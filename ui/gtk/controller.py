# -*- coding: utf-8 -*-
try:
    import gtk
except ImportError:
    print "You don't have GTK installed"

import pygtk
pygtk.require('2.0')

from calibrator.calibrator import Calibrator
from settings import DUALCLICK_THRESHOLD, FINGER_DELTA, MISCLICK_THRESHOLD, \
    NPOINTS, FULLSCREEN


class Window():

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.close_application)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)

        if FULLSCREEN:
            self.window.fullscreen()

        self.drawing_area = gtk.DrawingArea()
        self.window.add(self.drawing_area)
        self.window.show_all()

        self.drawable = self.drawing_area.window
        self.gc = self.drawing_area.get_style().fg_gc[gtk.STATE_NORMAL]

        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK |
                               gtk.gdk.BUTTON_PRESS_MASK)
        self.window.connect('button-press-event', self.on_button_pressed)
        self.window.connect('button-release-event', self.on_button_released)

        self.calibrator = Calibrator(NPOINTS, MISCLICK_THRESHOLD,
                                     DUALCLICK_THRESHOLD, FINGER_DELTA)

        screen = self.window.get_screen()
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.calibrator.set_screen_prop(self.width, self.height)

        self.status = None
        self.next = (0, 0)

        gtk.main()

    def draw_pointer(self, (centerx, centery)):
        drawable = self.drawable
        gc = self.gc

        x1 = centerx - 24
        x2 = centerx + 24
        y1 = centery - 24
        y2 = centery + 24
        r = 10

        drawable.draw_line(gc, centerx, y1, centerx, y2)
        drawable.draw_line(gc, x1, centery, x2, centery)
        drawable.draw_arc(gc, False, centerx-r/2, centery-r/2, r, r, 0, 360*64)

    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def on_button_pressed(self, widget, event):
        if event.button == 1 and self.status == 'calibrating':
            data = (event.x_root, event.y_root)
            error = self.calibrator.add_click(data)
            if error is None:
                print "Click valid: ", data
                self.next = self.calibrator.get_next_point()
            elif error == 'misclick':
                print "Misclick detected: ", data
                self.error("Misclick detected: " + str(data))
                #self.send_command('misclick', data)
            elif error == 'doubleclick':
                print "Doubleclick detected: ", data
                self.error("Doubleclick detected: " + str(data))
                #self.send_command('doubleclick', data)
            return True
        else:
            self.status = 'calibrating'
            self.next = self.calibrator.get_next_point()

    def on_button_released(self, widget, event):
        if event.button == 1:
            self.drawable.clear()
            if self.next is None:
                self.finish()
                quit()
            else:
                self.draw_pointer(self.next)
        return True

    def error(self, msg):
        drawable = self.drawable
        gc = self.gc

        width = 200
        height = 100
        font = gtk.load_font(
            "-misc-fixed-medium-r-*-*-*-140-*-*-*-*-iso8859-1")

        drawable.draw_rectangle(gc, False, self.width / 2 - width / 2,
                                self.height / 2 - height / 2, width, height)
        drawable.draw_text(font, gc, self.width / 2 - len(msg),
                           self.height / 2 - len(msg), msg)

    def finish(self):
        self.calibrator.calc_new_axis()
        self.calibrator.finish()
