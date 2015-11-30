# -*- coding: utf-8 -*-

"""
    This script uses brute force to verify what actions take to make a correct
    calibration.

    Operations:
    Perfect Screen Quadrants    Invert X     Invert Y     Swap XY
          +---+---+             +---+---+    +---+---+    +---+---+
          | 1 | 2 |             | 2 | 1 |    | 3 | 4 |    | 1 | 3 |
          +---+---+             +---+---+    +---+---+    +---+---+
          | 3 | 4 |             | 4 | 3 |    | 1 | 2 |    | 2 | 4 |
          +---+---+             +---+---+    +---+---+    +---+---+


"""
from __future__ import print_function
from __future__ import absolute_import
from six.moves import range


def distinct(a, b, c, d):
    if a != b and a != c and a != d and b != c and b != d and c != d:
        return True
    else:
        return False


def invertx(m):
    m_x = [[m[0][1], m[0][0]],
           [m[1][1], m[1][0]]]
    return m_x


def inverty(m):
    m_y = [[m[1][0], m[1][1]],
           [m[0][0], m[0][1]]]
    return m_y


def swapxy(m):
    m_s = [[m[0][0], m[1][0]],
           [m[0][1], m[1][1]]]
    return m_s


def get_cases(n):
    cases = []
    items = list(range(n))
    for a in items:
        for b in items:
            for c in items:
                for d in items:
                    if distinct(a, b, c, d):
                        cases.append([[a+1, b+1],
                                      [c+1, d+1]])
    return cases


def printable(m):
    return '{}{}{}{}'.format(m[0][0], m[0][1], m[1][0], m[1][1])


def main():
    mods_list = [[],
                 [invertx],
                 [inverty],
                 [invertx, inverty],
                 [swapxy],
                 [swapxy, invertx],
                 [swapxy, inverty],
                 [swapxy, inverty, invertx]]
    cases = get_cases(4)
    perfect = [[1, 2],
               [3, 4]]
    for case in cases:
        for i, mods in enumerate(mods_list):
            m = case
            for mod in mods:
                m = mod(m)
            if m == perfect:
                print(printable(case), [m.__name__ for m in mods])

main()
