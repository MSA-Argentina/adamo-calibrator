from argparse import ArgumentParser

from adamo_calibrator.settings import FAST_START, MISCLICK_THRESHOLD, \
    DUALCLICK_THRESHOLD, TIMEOUT, FINGER_DELTA, AUTO_CLOSE

parser = ArgumentParser()
group_ui = parser.add_mutually_exclusive_group()
group_dev = parser.add_mutually_exclusive_group()

group_dev.add_argument('--device', type=int, metavar='dev-id', default=None,
                       help='Set device ID manually for calibration.')
group_dev.add_argument('--fake', action="store_true",
                       help="Use a fake device.")
parser.add_argument('--dualclick', type=int, metavar='threshold',
                    default=DUALCLICK_THRESHOLD,
                    help='Set dualclick threshold.')
parser.add_argument('--misclick', type=int, metavar='threshold',
                    default=MISCLICK_THRESHOLD, help='Set misclick threshold.')
parser.add_argument('--faststart', action="store_true", default=FAST_START,
                    help="Start calibrating.")
parser.add_argument('--autoclose', action="store_true", default=AUTO_CLOSE,
                    help="Close without user click.")
group_ui.add_argument('-g', '--gui', choices=['gtk', 'web'],
                      help='Set GUI.')
group_ui.add_argument('-l', '--list', action="store_true",
                      help='List calibratables devices available.')
parser.add_argument('--timeout', type=int, metavar='milliseconds',
                    default=TIMEOUT,
                    help='Set timeout in milliseconds. (0 for disable)')

args = parser.parse_args()

if args.list:
    from adamo_calibrator.export.xinput import XInput
    devices = XInput.get_device_with_prop('Evdev Axis Calibration',
                                          id_only=False)
    print "Devices:"
    for name, id, setted in devices:
        print("\tId: {0:2}\tName: {1}".format(id, name))
    quit()

if args.gui == 'gtk':
    from adamo_calibrator.ui.run_gtk import run_gtk as run
else:
    from adamo_calibrator.ui.run_zaguan import run_web as run

run(fake=args.fake, device=args.device, misclick_threshold=args.misclick,
    dualclick_threshold=args.dualclick, finger_delta=FINGER_DELTA,
    timeout=args.timeout, fast_start=args.faststart, auto_close=args.autoclose)
