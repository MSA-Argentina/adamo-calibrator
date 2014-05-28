from sys import argv

parameters = """Adamo Calibrator
Help:
    -h, --help: Print this help message.
    -v, --verbose: Print debug messages during calibration process.
    --list: List calibratables input devices.
    --device <id>: Select a specific device to calibrate.
    --manual <x_min, x_max, y_min, y_max>: Set manual calibration values.
    --misclick <threshold>: Set misclick threshold.
    --output <xinput>: Set type of output setting.
    --gui <web|gtk>: Set gui interface.
"""


def error():
    print "Error."

if '-h' in argv or '--help' in argv:
    print parameters
    quit()
if '-v' in argv or '--verbose' in argv:
    DEBUG = True
if '--list' in argv:
    from export.xinput import XInput
    devices = XInput().get_device_with_prop('Evdev Axis Calibration',
                                            id_only=False)
    print "Devices:"
    for name, id in devices:
        print("\tId: {0:2}\tName: {1}".format(id, name))
if '--device' in argv:
    idx = argv.index('--device')
    device = argv[idx + 1]
if '--manual' in argv:
    print "MANUAL"
if '--output' in argv:
    idx = argv.index('--output')
    output_type = argv[idx + 1]
else:
    output_type = 'xinput'
if '--gui' in argv:
    idx = argv.index('--gui')
    interface = argv[idx + 1]
    if interface == 'web':
        from ui.run_zaguan import run_web as run
    elif interface == 'gtk':
        from ui.run_gtk import run_gtk as run
    else:
        run = error
    run()
else:
    from ui.run_gtk import run_gtk
    run_gtk()
