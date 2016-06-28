from __future__ import absolute_import
from __future__ import print_function

from os import popen

from .settings import FAKE, TEST


class XInput(object):
    @staticmethod
    def get_device_with_prop(prop, id_only=True):
        devices = []
        proc = popen('xinput list --id-only')
        stdout = proc.read()
        dev_ids = stdout.split('\n')[0:-1]

        # Searching Virtual core keboard.
        idx = dev_ids.index('3')
        dev_ids = dev_ids[:idx]
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
                    if prop in property:
                        if '<no items>' not in property:
                            setted = False
                        else:
                            setted = True

                        if id_only:
                            devices.append((id, setted))
                        else:
                            devices.append((dev_names[i], id, setted))
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
    def get_prop_range(dev_id):
        value = []
        proc = popen('xinput list --long  %s' % dev_id)
        stdout = proc.read()
        stdout = stdout.split('\n')
        for line in stdout:
            if 'Range' in line:
                str_range = line.split(':')[1]
                str_range = str_range.replace(' ', '')
                axis_range = str_range.split('-')
                value += axis_range
        return value[:4]

    @staticmethod
    def set_prop(dev_id, property, data):
        print('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))
        if not FAKE and not TEST:
            popen('xinput set-prop {0} {1} {2}'.format(dev_id, property, data))

    @staticmethod
    def get_dev_vendor(dev_id):
        cmd = 'xinput list-props {} | grep "Device Node" | cut -d ":" -f 2'.\
            format(dev_id)
        proc = popen(cmd)
        stdout = proc.read().strip()
        stdout = stdout.replace('\"', '')
        event = stdout.split('/')[-1]

        cmd = 'grep -E "Handlers|Bus=" /proc/bus/input/devices | grep -B1 ' \
              '"{}" | head -n 1 | cut -d ":" -f 2'.format(event)
        proc = popen(cmd)
        stdout = proc.read().strip()
        dev = stdout.split()
        dev = [d.split('=')[1] for d in dev]
        dev = {'bus': dev[0],
               'vendor': dev[1],
               'product': dev[2],
               'version': dev[3]}

        return dev
