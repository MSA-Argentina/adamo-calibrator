from __future__ import absolute_import
from __future__ import print_function

from random import randint
from sys import exit

from .constants import calc
from .export import XInput
from .helpers import calc_quadrant, get_adyacent, same_axis, scale_axis


class Calibrator:
    """ Calibrator main class """

    def __init__(self, npoints, threshold_misclick, threshold_doubleclick,
                 device=None, fake=False):
        """ Constructor """

        # Screen properties
        self.width = None
        self.height = None

        # Clicks configurations
        self.npoints = npoints
        self.threshold_misclick = threshold_misclick
        self.threshold_doubleclick = threshold_doubleclick
        self.blocks = 8

        # Calibration data
        self.nclicks = 0
        self.clicks = {}
        self.points = []
        self.points_clicked = []

        # Calibration actions
        self.swapxy = False
        self.inversex = False
        self.inversey = False

        # Getting device base properties
        if fake:
            self.device = 'fake'
            self.old_prop_value = [0, 1000, 0, 1000]
        elif device is not None:
            self.device = device
            self.__get_device_prop_range()
        else:
            self.__get_device()

    def __get_device(self):
        """ Loads a calibratable device from XInput.
            In case of more than one devices are connected on the computer,
            this'll select the last one.
        """

        devices = XInput.get_device_with_prop('Evdev Axis Calibration',
                                              False)
        if not devices:
            print("Error: No calibratable devices found.")
            exit()
        elif len(devices) > 1:
            print("More than one devices detected. Using lastone.")

        # Get device with format (Name, DevID, setted)
        self.device = devices[-1][1]
        self.__get_device_prop_range()
        # This reset calibration to defaults values because recalibration
        # errors
        self.__reset_device_calibration()

    def __get_device_prop_range(self):
        """ Get the value range of the calibration property of the device.
        """

        self.old_prop_value = XInput.get_prop_range(self.device)

    def __reset_device_calibration(self):
        """ Reset the calibration data of the device.
        """

        XInput.set_prop(self.device, '"Evdev Axes Swap"', '0')
        XInput.set_prop(self.device, '"Evdev Axis Inversion"', '0, 0')
        XInput.set_prop(self.device, '"Evdev Axis Calibration"',
                        '{0} {1} {2} {3}'.format(
                            int(float(self.old_prop_value[0])),
                            int(float(self.old_prop_value[1])),
                            int(float(self.old_prop_value[2])),
                            int(float(self.old_prop_value[3]))))

    def set_screen_prop(self, width, height):
        """ Set the screen width and height and get calculated points and the
            respective separation between them.
        """

        self.width = width
        self.height = height

        block_x = width / self.blocks
        block_y = height / self.blocks

        self.points = [(block_x, block_y),
                       (block_x, block_y * 7),
                       (block_x * 7, block_y),
                       (block_x * 7, block_y * 7)]

    def reset(self):
        """ Reset all calibration data
        """

        # Resetting calibration data
        self.nclicks = 0
        self.clicks = {}
        self.points = []
        self.points_clicked = []

        # Resetting calibration actions
        self.swapxy = False
        self.inversex = False
        self.inversey = False

        self.__reset_device_calibration()
        self.set_screen_prop(self.width, self.height)

    def __doubleclick(self, x, y):
        """ Detects if a doubleclick was made based in a threshold.
        """

        doubleclick = False
        clicks = self.clicks
        for key in clicks:
            (xc, yc) = clicks[key]
            if (abs(x - xc) < self.threshold_doubleclick and
                    abs(y - yc) < self.threshold_doubleclick):
                doubleclick = True
        return doubleclick

    def __misclick(self, x, y):
        """ Detects if a misclick was made based in a threshold.
        """

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

    def add_click(self, click):
        """ Register a new click made by user and return an error
            if it's need.
        """

        (x, y) = click
        error = None
        if self.__doubleclick(x, y):
            error = 'doubleclick'
        elif self.__misclick(x, y):
            error = 'misclick'
        else:
            expected = self.points_clicked[-1]
            self.clicks[expected] = (x, y)
            self.nclicks += 1
        return error

    def get_next_point(self):
        """ Returns the next point if is available.
        """

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

    def __check_axis(self):
        """ Checks if a inversion of axis or swapping of axis is needed.
            Getting the keys ordered by quadrant.
        """

        ordered_keys = sorted(self.clicks, key=lambda k: (k[1], k[0]))

        # Making the key
        calc_key = ''
        for key in ordered_keys:
            x, y = self.clicks[key]
            calc_key += '{}'.format(calc_quadrant(self.width, self.height, x,
                                                  y))

        # Getting the settings.
        self.inversex, self.inversey, self.swapxy = calc[calc_key]

    def __calc_new_axis(self):
        """ Get the new calculated axis.
            This is done using the old axis data and clicks made in the
            calibration process.
        """

        # Screen properties
        width = self.width
        height = self.height

        # Old calibration data
        old_xmin = int(float(self.old_prop_value[0]))
        old_xmax = int(float(self.old_prop_value[1]))
        old_ymin = int(float(self.old_prop_value[2]))
        old_ymax = int(float(self.old_prop_value[3]))

        # Processing clicks data
        clicks = self.clicks
        clicks_x = [clicks[x, y][0] for x, y in clicks]
        clicks_y = [clicks[x, y][1] for x, y in clicks]
        clicks_x.sort()
        clicks_y.sort()

        # Verifying the axes corresponding
        x_min = float(clicks_x[0] + clicks_x[1])/2
        x_max = float(clicks_x[2] + clicks_x[3])/2
        y_min = float(clicks_y[0] + clicks_y[1])/2
        y_max = float(clicks_y[2] + clicks_y[3])/2

        # Swapping axes if necessary
        if (abs(clicks_x[0] - clicks_x[3]) < abs(clicks_y[0] - clicks_y[3])):
            self.swapxy = not(self.swapxy)
            x_min, y_min = y_min, x_min
            x_max, y_max = y_max, x_max

        # Calculating separation of dot axes
        block_x = float(width) / self.blocks
        block_y = float(height) / self.blocks

        # Calculating the new calibration data
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

    def finish(self):
        """ Save a new axis reference.
        """

        self.__calc_new_axis()
        self.__check_axis()

        inversex = 1 if self.inversex else 0
        inversey = 1 if self.inversey else 0
        x_min = self.x_min
        x_max = self.x_max
        y_min = self.y_min
        y_max = self.y_max

        if self.swapxy:
            XInput.set_prop(self.device, '"Evdev Axes Swap"', '1')
            inversex, inversey = inversey, inversex
            x_min, y_min = y_min, x_min
            x_max, y_max = y_max, x_max

        if self.inversex or self.inversey:
            XInput.set_prop(self.device, '"Evdev Axis Inversion"',
                            '{0}, {1}'.format(inversex, inversey))
        XInput.set_prop(self.device, '"Evdev Axis Calibration"',
                        '{0} {1} {2} {3}'.format(x_min, x_max,
                                                 y_min, y_max))
