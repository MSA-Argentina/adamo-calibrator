from os import popen
from settings import TEST


class XInput(object):
    @staticmethod
    def get_device_with_prop(prop, id_only=True):
        devices = []
        proc = popen('xinput list --id-only')
        stdout = proc.read()
        dev_ids = stdout.split('\n')[0:-1]
        if not id_only:
            proc = popen('xinput list --name-only')
            stdout = proc.read()
            dev_names = stdout.split('\n')[0:-1]

        for i, id in enumerate(dev_ids):
            proc = popen('xinput list-props %s' % id)
            stdout = proc.read()
            if prop in stdout:
                stdout = stdout.split('\n')
                for property in stdout:
                    if prop in property and '<no items>' not in property:
                        if id_only:
                            devices.append(id)
                        else:
                            devices.append((dev_names[i], id))
                        break
        return devices

    @staticmethod
    def get_prop(dev_id, prop):
        value = None
        proc = popen('xinput list-props  %s' % dev_id)
        stdout = proc.read()
        if prop in stdout:
            stdout = stdout.split('\n')
            for property in stdout:
                if prop in property:
                    value = property.split(':')[1]
                    value = value.replace('\t', '')
                    value = value.split(',')
                    break
        return value

    @staticmethod
    def set_prop(dev_id, property, data):
        print('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))
        if not TEST:
            popen('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))
