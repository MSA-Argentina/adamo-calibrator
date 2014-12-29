# -*- coding: utf-8 -*-

"""
    This dictionary is based in all cases returned by
    tools/axes_inversion_verification.py, every key has a tuple with
    axis inversion and axes swaping.
    Key Structure: Key is composed by the sum of calculated quadrants.
    Tuple Structure: (Inverse_X, Inverse_Y, Swap_XY)
"""

calc = {'1234': (False, False, False),
        '1324': (False, False, True),
        '2143': (True, False, False),
        '2413': (True, False, True),
        '3142': (False, False, True),
        '3412': (False, True, False),
        '4231': (True, True, True),
        '4321': (True, True, False)}
