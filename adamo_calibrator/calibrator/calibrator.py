from adamo_calibrator.calibrator.helpers import calc_quadrant, get_adyacent, \
    same_axis, scale_axis
from adamo_calibrator.export.xinput import XInput
from random import randint
from sys import exit


class Calibrator:

    def __init__(self, npoints, threshold_misclick, threshold_doubleclick,
                 delta_f, device=None, fake=False):
        self.width = None
        self.height = None

        self.npoints = npoints
        self.threshold_misclick = threshold_misclick
        self.threshold_doubleclick = threshold_doubleclick

        self.blocks = 8
        self.nclicks = 0
        self.clicks = {}
        self.points = []
        self.points_clicked = []
        self.swapxy = False
        self.inversex = False
        self.inversey = False

        if fake:
            self.device = 'fake'
            self.old_prop_value = [0, 1000, 0, 1000]
        elif device is not None:
            self.device = device
            self.get_device_prop()
        else:
            self.get_device()

    def get_device(self):
        #This function loads an calibratable device from xinput, if detect more
        #than one device, this select the first.
        devices = XInput.get_device_with_prop('Evdev Axis Calibration')
        if len(devices) == 0:
            print "Error: No calibratable devices found."
            exit()
        if len(devices) > 1:
            print "More than one devices detected. Using last."

        (self.device, setted) = devices[-1]
        if setted:
            self.get_device_prop()
        else:
            self.get_device_prop_range()

    def get_device_prop(self):
        self.old_prop_value = XInput.get_prop(self.device,
                                              'Evdev Axis Calibration')
        #If length of old_prop_value is lower than 4, get axis range
        if len(self.old_prop_value) < 4:
            self.get_device_prop_range()

    def get_device_prop_range(self):
        self.old_prop_value = XInput.get_prop_range(self.device)

    def set_screen_prop(self, width, height):
        #This function set the screen width and height and realize some
        #calcules respecting of points and the separation between this
        self.width = width
        self.height = height

        block_x = width / self.blocks
        block_y = height / self.blocks

        self.points = [(block_x, block_y),
                       (block_x, block_y * 7),
                       (block_x * 7, block_y),
                       (block_x * 7, block_y * 7)]

    def calc_new_axis(self):
        #This function calcules a new axis of references, based on clicks and
        #old axis references witch uses in a transform with new axis
        width = self.width
        height = self.height

        old_xmin = int(float(self.old_prop_value[0]))
        old_xmax = int(float(self.old_prop_value[1]))
        old_ymin = int(float(self.old_prop_value[2]))
        old_ymax = int(float(self.old_prop_value[3]))

        clicks = self.clicks
        clicks_x = [clicks[x, y][0] for x, y in clicks]
        clicks_y = [clicks[x, y][1] for x, y in clicks]
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
        #This function detects if a doubleclick was made
        doubleclick = False
        clicks = self.clicks
        for key in clicks:
            (xc, yc) = clicks[key]
            if (abs(x - xc) < self.threshold_doubleclick and
                    abs(y - yc) < self.threshold_doubleclick):
                doubleclick = True
        return doubleclick

    def misclick(self, x, y):
        #This function detects if a misclick was made.
        nclicks = self.nclicks
        threshold = self.threshold_misclick
        misclick = False
        if nclicks > 0:
            clicks = self.clicks
            point = self.points_clicked[-1]
            adyacents_points = get_adyacent(point, self.points_clicked[:-1])
            for adyacent_point in adyacents_points:
                if adyacent_point in clicks:
                    if not(same_axis(threshold, x, clicks[adyacent_point][0],
                                     clicks[adyacent_point][1]) or
                            same_axis(threshold, y, clicks[adyacent_point][0],
                                      clicks[adyacent_point][1])):
                        misclick = True

        return misclick

    def reset(self):
        width = self.width
        height = self.height
        self.clicks = {}
        self.points = []
        self.points_clicked = []
        self.nclicks = 0
        self.set_screen_prop(width, height)

    def check_axis(self, x, y):
        #This function checks if a inversion of axis or swapping of axis is
        #needed.
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
        #This function register a new click made by user and return an error
        #if it's need
        (x, y) = click
        error = None
        if self.doubleclick(x, y):
            error = 'doubleclick'
        elif self.misclick(x, y):
            error = 'misclick'
        else:
            expected = self.points_clicked[-1]
            self.clicks[expected] = (x, y)
            self.nclicks += 1
            self.check_axis(x, y)
        return error

    def get_next_point(self):
        #This function returns the next point if is available
        if len(self.points) > 0:
            if len(self.points_clicked) == 0:
                point = self.points.pop(randint(0, len(self.points) - 1))
                self.points_clicked.append(point)
            else:
                last = self.points_clicked[-1]
                adyacents = get_adyacent(last, self.points)
                point = adyacents.pop(randint(0, len(adyacents) - 1))
                self.points.pop(self.points.index(point))
                self.points_clicked.append(point)
        else:
            point = None
        return point

    def finish(self):
        #This function save a new axis reference and inverse the values if
        #need.
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
