
def calc_quadrant(w, h, x, y):
    """ Screen Quadrants
        +---+---+       1) x < w/2 && y < h/2
        | 1 | 2 |       2) x > w/2 && y < h/2
        +---+---+       3) x < w/2 && y > h/2
        | 3 | 4 |       4) x > w/2 && y > h/2
        +---+---+
    """
    if (x - w / 2) < 0 and (y - h / 2) < 0:
        quadrant = 1
    elif (x - w / 2) > 0 and (y - h / 2) < 0:
        quadrant = 2
    elif (x - w / 2) < 0 and (y - h / 2) > 0:
        quadrant = 3
    elif (x - w / 2) > 0 and (y - h / 2) > 0:
        quadrant = 4
    return quadrant


def get_adyacent(x_and_y, points):
    (x, y) = x_and_y
    adyacents = []
    for point in points:
        if x == point[0] or y == point[1]:
            adyacents.append(point)
    return adyacents


def same_axis(threshold, x, xp, yp):
    same_axis = False
    if abs(x - xp) < threshold or abs(x - yp) < threshold:
        same_axis = True
    return same_axis


def scale_axis(cx, to_max, to_min, from_max, from_min):
    to_width = to_max - to_min
    from_width = from_max - from_min
    if (from_width):
        x = int(((to_width * (cx - from_min) / from_width)) + to_min)
    else:
        x = 0
    if (x > to_max):
        x = to_max
    if (x < to_min):
        x = to_min
    return x


def printable(a, b, c, d):
    return '{}{}{}{}'.format(a, b, c, d)
