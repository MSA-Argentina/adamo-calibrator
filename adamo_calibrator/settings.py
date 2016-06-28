from __future__ import absolute_import
from os.path import join, split

TEST = False
FAKE = False

DEBUG = True
FULLSCREEN = True
SHOW_CURSOR = True

NPOINTS = 5
MISCLICK_THRESHOLD = 30
DUALCLICK_THRESHOLD = 100

# Timeout in milliseconds
TIMEOUT = 0

# Internationalization Settings
PO_NAME = 'calibrator'
DEFAULT_LOCALE = 'en_US'
RESOURCES_PATH = join(split(__file__)[0], 'resources')

FAST_START = True
AUTO_CLOSE = True
