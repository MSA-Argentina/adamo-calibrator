from xinput import XInput
from random import randint


class Calibrator:

    def __init__(self, npoints, threshold_misclick, threshold_doubleclick):
        self.width = None
        self.height = None
        self.device = None

        self.npoints = npoints
        self.threshold_misclick = threshold_misclick
        self.threshold_doubleclick = threshold_doubleclick

        self.blocks = 8
        self.nclicks = 0
        self.clicks = []
        self.points = []
        self.points_clicked = []
        self.swapxy = False

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

    def calc_new_axis(self, old_xmin, old_xmax, old_ymin, old_ymax):
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
        return error

    def get_next_point(self):
        if len(self.points) > 0:
            point = self.points.pop(randint(0, len(self.points) - 1))
            self.points_clicked.append(point)
        else:
            point = None
        return point

    def get_device(self):
        #TODO:
        #Esta funcion debe conectarse con la clase xedev que devuelve el id o
        #el nombre del dispositivo
        pass

    def get_properties(self):
        #TODO:
        #Esta funcion debe conectarse con la clase xedev que devuelve las
        #configuraciones antiguas
        pass

    def finish(self):
        #TODO:
        #Esta funcion debe conectarse con la clase xedev que guarde las
        #settings
        if self.swapxy:
            XInput().set_prop('"Evdev Axis Calibration"', '10',
                              '{0} {1} {2} {3}'.format(self.x_min, self.x_max,
                                                       self.y_min, self.y_max))
            XInput().set_prop('"Evdev Axes Swap"', '10', '1')
            XInput().set_prop('"Evdev Axis Inverse"', '10', '0, 1')
        else:
            XInput().set_prop('"Evdev Axis Calibration"', '10',
                              '{0} {1} {2} {3}'.format(self.x_min, self.x_max,
                                                       self.y_min, self.y_max))
