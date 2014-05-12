from evdev import InputDevice, list_devices

class XInput:

    def get_device():
        devices = map(InputDevice, list_devices())

    def get_prop():
        pass

    def set_prop(self, property, device, data):
        print "xinput set-prop", device, property, " ".join(data)
