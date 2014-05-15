from xinput import XInput
from random import randint


class Calibrator:

    def __init__(self, npoints, threshold_misclick, threshold_doubleclick,
                 delta_f):
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

        self.delta_x = None
        self.delta_y = None
        self.delta_f = delta_f

        self.get_device()

    def get_device(self):
        xinput = XInput()
        devices = xinput.get_device_with_prop('Evdev Axis Calibration')
        if len(devices) == 0:
            print "Error: No calibratable devices found."
            quit()
        if len(devices) > 1:
            print "More than one devices detected. Using last."
            self.device = devices[1]
        else:
            self.device = devices[0]

        self.old_prop_value = xinput.get_prop(self.device,
                                              'Evdev Axis Calibration')

    def set_screen_prop(self, width, height):
        self.width = width
        self.height = height

        self.delta_x = width / self.blocks
        self.delta_y = height / self.blocks

        self.points = [(self.delta_x, self.delta_y),
                       (self.delta_x, self.delta_y * 7),
                       (self.delta_x * 7, self.delta_y),
                       (self.delta_x * 7, self.delta_y * 7)]

    def calc_new_axis(self):
        def scale_axis(cx, to_max, to_min, from_max, from_min):
            to_width = to_max - to_min
            from_width = from_max - from_min

            if (from_width):
                x = int(((to_width * (cx - from_min) / from_width)) + to_min)
            else:
                x = 0

            if (x > to_max):
                x = to_max
            if (x < to_min):
                x = to_min

            return x

        width = self.width
        height = self.height

        old_xmin = int(self.old_prop_value[0])
        old_xmax = int(self.old_prop_value[1])
        old_ymin = int(self.old_prop_value[2])
        old_ymax = int(self.old_prop_value[3])

        clicks_x = [x for x, y in self.clicks]
        clicks_y = [y for x, y in self.clicks]
        clicks_x.sort()
        clicks_y.sort()

        x_min = float(clicks_x[0] + clicks_x[1])/2
        x_max = float(clicks_x[2] + clicks_x[3])/2
        y_min = float(clicks_y[0] + clicks_y[1])/2
        y_max = float(clicks_y[2] + clicks_y[3])/2

        if (abs(clicks_x[0] - clicks_x[3]) < abs(clicks_y[0] - clicks_y[3])):
            self.swapxy = not(self.swapxy)
            x_min, y_min = y_min, x_min
            x_max, y_max = y_max, x_max

        block_x = float(width) / self.blocks
        block_y = float(height) / self.blocks

        scale_x = (x_max - x_min) / (width - 2 * block_x)
        x_min -= block_x * scale_x
        x_max += block_x * scale_x
        scale_y = (y_max - y_min) / (height - 2 * block_y)
        y_min -= block_y * scale_y
        y_max += block_y * scale_y

        self.x_min = scale_axis(x_min, old_xmax, old_xmin, width, 0)
        self.x_max = scale_axis(x_max, old_xmax, old_xmin, width, 0)
        self.y_min = scale_axis(y_min, old_ymax, old_ymin, height, 0)
        self.y_max = scale_axis(y_max, old_ymax, old_ymin, height, 0)

    def doubleclick(self, x, y):
        doubleclick = False
        for (xc, yc) in self.clicks:
            if (abs(x - xc) < self.threshold_misclick and
                    abs(y - yc) < self.threshold_misclick):
                doubleclick = True
        return doubleclick

    def misclick(self, x, y):
        def in_zone(threshold, x, y, xc, yc):
            in_zone = False
            if (xc - threshold) <= x <= (xc + threshold) and \
                    (yc - threshold) <= y <= (yc + threshold):
                in_zone = True
            return in_zone

        nclicks = self.nclicks
        if nclicks > 0:
            misclick = True
            clicks = self.points + [self.points_clicked[-1]]
            for click in clicks:
                if in_zone(self.threshold_misclick, x, y, click[0], click[1]):
                    misclick = False
        else:
            misclick = False
        return misclick

    def check_axis(self, x, y):
        def calc_quadrant(w, h, x, y):
            if (x - w / 2) > 0 and (y - h / 2) < 0:
                quadrant = 1
            elif (x - w / 2) < 0 and (y - h / 2) < 0:
                quadrant = 2
            elif (x - w / 2) < 0 and (y - h / 2) > 0:
                quadrant = 3
            elif (x - w / 2) > 0 and (y - h / 2) > 0:
                quadrant = 4
            return quadrant

        (xp, yp) = self.points_clicked[-1]
        quadrant_exp = calc_quadrant(self.width, self.height, xp, yp)
        quadrant = calc_quadrant(self.width, self.height, x, y)
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
        elif (quadrant == quadrant_exp):
            self.inversex = False
            self.inversey = False
            self.swapxy = False

    def add_click(self, click):
        (x, y) = click
        error = None
        if self.doubleclick(x, y):
            error = 'doubleclick'
        elif self.misclick(x, y):
            error = 'misclick'
        else:
            self.clicks.append((x, y))
            self.nclicks += 1
            self.check_axis(x, y)
        return error

    def get_next_point(self):
        if len(self.points) > 0:
            point = self.points.pop(randint(0, len(self.points) - 1))
            self.points_clicked.append(point)
        else:
            point = None
        return point

    def finish(self):
        xinput = XInput()
        inversex = 1 if self.inversex else 0
        inversey = 1 if self.inversey else 0
        x_min = self.x_min
        x_max = self.x_max
        y_min = self.y_min
        y_max = self.y_max

        if self.swapxy:
            xinput.set_prop(self.device, '"Evdev Axes Swap"', '1')
            inversex, inversey = inversey, inversex
            x_min, y_min = y_min, x_min
            x_max, y_max = y_max, x_max

        if self.inversex or self.inversey:
            xinput.set_prop(self.device, '"Evdev Axis Inversion"',
                            '{0}, {1}'.format(inversex, inversey))
        xinput.set_prop(self.device, '"Evdev Axis Calibration"',
                        '{0} {1} {2} {3}'.format(x_min, x_max,
                                                 y_min, y_max))
