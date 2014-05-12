from xinput import XInput


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

    def set_screen_prop(self, width, height):
        self.width = width
        self.height = height

        self.delta_x = width / self.blocks
        self.delta_y = height / self.blocks

    def calc_new_axis(self, old_xmin, old_xmax, old_ymin, old_ymax):
        clicks = self.clicks
        delta_x = self.delta_x
        delta_y = self.delta_y

        scale_x = (old_xmax - old_xmin) * 1.0 / self.width
        scale_y = (old_ymax - old_ymin) * 1.0 / self.height

        self.x_min = int((clicks[0][0] + clicks[2][0])/2 * scale_x) - delta_x
        self.x_max = int((clicks[1][0] + clicks[3][0])/2 * scale_x) + delta_x
        self.y_min = int((clicks[0][1] + clicks[1][1])/2 * scale_y) - delta_y
        self.y_max = int((clicks[2][1] + clicks[3][1])/2 * scale_y) + delta_y

    def doubleclick(self, x, y):
        for (xc, yc) in self.clicks:
            if (abs(x - xc) < self.threshold_misclick and
                    abs(y - yc) < self.threshold_misclick):
                return True
        return False

    def misclick(self, x, y, xe, ye):
        if (abs(x - xe) < self.threshold_misclick and
                abs(y - ye) < self.threshold_misclick):
            return True
        return False

    def add_click(self, click):
        (x, y) = click
        #Implementar misclick, pero hay que calcular el esperado
        if not self.doubleclick(x, y):
            self.clicks.append((x, y))
            self.nclicks += 1
            print 'Click added X: ', x, 'Y: ', y
        else:
            print 'Misclick detected X: ', x, 'Y: ', y

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
        XInput().set_prop('"Evdev Axis Calibration"', '10', [str(self.x_min),
                                                             str(self.x_max),
                                                             str(self.y_min),
                                                             str(self.y_max)])
