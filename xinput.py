from os import popen


class XInput:

    def get_device_with_prop(self, prop):
        devices = []
        proc = popen('xinput list --id-only')
        stdout = proc.read()
        dev_ids = stdout.split('\n')[0:-1]

        for id in dev_ids:
            proc = popen('xinput list-props %s' % id)
            stdout = proc.read()
            if prop in stdout:
                stdout = stdout.split('\n')
                for property in stdout:
                    if prop in property and '<no items>' not in property:
                        devices.append(id)
                        break
        return devices

    def get_prop(self, dev_id, prop):
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

    def set_prop(self, dev_id, property, data):
        print('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))
        popen('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))
