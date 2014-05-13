from xinput import XInput
from random import randint


class Calibrator:

    def __init__(self, npoints, threshold_misclick, threshold_doubleclick):
        self.width = None
        self.height = None

        self.npoints = npoints
        self.threshold_misclick = threshold_misclick
        self.threshold_doubleclick = threshold_doubleclick

        self.blocks = 8
        self.nclicks = 0
        self.clicks = []
        self.points = []
        self.points_clicked = []
        self.swapxy = False
        self.inversex = False
        self.inversey = False

        xinput = XInput()
        self.devices = xinput.get_device_with_prop('Evdev Axis Calibration')
        self.old_prop_value = xinput.get_prop(self.devices[0],
                                              'Evdev Axis Calibration')

    def set_screen_prop(self, width, height):
        self.width = width
        self.height = height

        self.delta_x = width / self.blocks
        self.delta_y = height / self.blocks

        self.points = [(self.delta_x, self.delta_y),
                       (self.delta_x, self.delta_y * 7),
                       #(self.delta_x * 4, self.delta_y * 4),
                       (self.delta_x * 7, self.delta_y),
                       (self.delta_x * 7, self.delta_y * 7)]

    def calc_new_axis(self):
        old_xmin = int(self.old_prop_value[0])
        old_xmax = int(self.old_prop_value[1])
        old_ymin = int(self.old_prop_value[2])
        old_ymax = int(self.old_prop_value[3])

        clicks_x = [x for x, y in self.clicks]
        clicks_y = [y for x, y in self.clicks]
        clicks_x.sort()
        clicks_y.sort()

        delta_x = self.delta_x
        delta_y = self.delta_y

        scale_x = (old_xmax - old_xmin) * 1.0 / self.width
        scale_y = (old_ymax - old_ymin) * 1.0 / self.height

        if (max(clicks_x) - min(clicks_x)) < (max(clicks_y) - min(clicks_y)):
            self.swapxy = True

        self.x_min = int(((clicks_x[0] + clicks_x[1])/2 - delta_x) * scale_x)
        self.x_max = int(((clicks_x[2] + clicks_x[3])/2 + delta_x) * scale_x)
        self.y_min = int(((clicks_y[0] + clicks_y[1])/2 - delta_y) * scale_y)
        self.y_max = int(((clicks_y[2] + clicks_y[3])/2 + delta_y) * scale_y)

    def doubleclick(self, x, y):
        doubleclick = False
        for (xc, yc) in self.clicks:
            if (abs(x - xc) < self.threshold_misclick and
                    abs(y - yc) < self.threshold_misclick):
                doubleclick = True
        return doubleclick

    def misclick(self, x, y, xe, ye):
        misclick = False
        nclicks = self.nclicks
        if nclicks > 0:
            if nclicks == 1:
                pass
            elif nclicks == 2:
                pass
            elif nclicks == 3:
                pass

        return misclick

    def calc_quadrant(self, x, y):
        width = self.width
        height = self.height
        if (x - width / 2) > 0 and (y - height / 2) < 0:
            quadrant = 1
        elif (x - width / 2) < 0 and (y - height / 2) < 0:
            quadrant = 2
        elif (x - width / 2) < 0 and (y - height / 2) > 0:
            quadrant = 3
        elif (x - width / 2) > 0 and (y - height / 2) > 0:
            quadrant = 4

        return quadrant

    def add_click(self, click):
        (x, y) = click
        (xp, yp) = self.points_clicked[-1]
        error = None
        if self.doubleclick(x, y):
            error = 'doubleclick'
        elif self.misclick(x, y, xp, yp):
            error = 'misclick'
        else:
            self.clicks.append((x, y))
            self.nclicks += 1
            quadrant_exp = self.calc_quadrant(xp, yp)
            quadrant = self.calc_quadrant(x, y)
            if (quadrant == 1 and quadrant_exp == 2) or \
                    (quadrant == 2 and quadrant_exp == 1) or \
                    (quadrant == 3 and quadrant_exp == 4) or \
                    (quadrant == 4 and quadrant_exp == 3):
                self.inversex = True
            elif (quadrant == 1 and quadrant_exp == 3) or \
                    (quadrant == 3 and quadrant_exp == 1) or \
                    (quadrant == 2 and quadrant_exp == 4) or \
                    (quadrant == 4 and quadrant_exp == 2):
                self.inversey = True
            elif (quadrant == 1 and quadrant_exp == 4) or \
                    (quadrant == 4 and quadrant_exp == 1) or \
                    (quadrant == 2 and quadrant_exp == 3) or \
                    (quadrant == 3 and quadrant_exp == 2):
                self.swapxy = True

        return error

    def get_next_point(self):
        if len(self.points) > 0:
            point = self.points.pop(randint(0, len(self.points) - 1))
            self.points_clicked.append(point)
        else:
            point = None
        return point

    def finish(self):
        XInput().set_prop(self.devices[0], '"Evdev Axis Calibration"',
                          '{0} {1} {2} {3}'.format(self.x_min, self.x_max,
                                                   self.y_min, self.y_max))
        if self.inversex:
            inversex = 1
        else:
            inversex = 0
        if self.inversey:
            inversey = 1
        else:
            inversey = 0
        if self.swapxy:
            XInput().set_prop(self.devices[0], '"Evdev Axes Swap"', '1')
            XInput().set_prop(self.devices[0], '"Evdev Axis Inversion"',
                              '{0}, {1}'.format(inversey, inversex))
        else:
            XInput().set_prop(self.devices[0], '"Evdev Axis Inversion"',
                              '{0}, {1}'.format(inversey, inversex))
