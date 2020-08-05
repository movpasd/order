import numpy as np
from multipledispatch import dispatch

from utils.floatshapes import FloatRect, FloatCircle


_ZEROVEC = np.array((0., 0.))


@dispatch(FloatRect, FloatRect)
def collidevector(a, b):

    flipx = a.cx < b.cx
    flipy = a.cy < b.cy

    dx = (b.left - a.right) if flipx else (b.right - a.left)
    dy = (b.bottom - a.top) if flipy else (b.top - a.bottom)

    if (flipx and dx > 0) or (not flipx and dx < 0):
        dx = 0.
    if (flipy and dy > 0) or (not flipy and dy < 0):
        dy = 0.

    if np.abs(dx) < np.abs(dy):
        return np.array((dx, 0.))
    else:
        return np.array((0., dy))


@dispatch(FloatCircle, FloatRect)
def collidevector(a, b):

    hw, hh = b.width / 2, b.height / 2
    dcx, dcy = a.center - b.center

    if np.abs(dcx) <= hw or np.abs(dcy) <= hh:
        return collidevector(a.get_rect(), b)
    
    if (np.abs(dcx) - hw)**2 + (np.abs(dcy) - hh)**2 < a.r**2:

        if (dcx >= 0 and dcy >= 0):
            corner = b.topright
        elif (dcx < 0 and dcy >= 0):
            corner = b.topleft
        elif (dcx >= 0 and dcy < 0):
            corner = b.bottomright
        elif (dcx < 0 and dcy < 0):
            corner = b.bottomleft

        dr = a.center - corner
        dx, dy = dr

        dist = np.sqrt(dx**2 + dy**2)
        return np.array((dx, dy)) * (a.r / dist - 1)

    return _ZEROVEC.copy()


@dispatch(FloatRect, FloatCircle)
def collidevector(a, b):

    return -collidevector(b, a)


@dispatch(FloatCircle, FloatCircle)
def collidevector(a, b):

    dx = a.cx - b.cx
    dy = a.cy - b.cy
    sqdist = dx**2 + dy**2
    radsum = a.r + b.r
    sqrad = radsum**2

    if sqdist < sqrad:

        dist = np.sqrt(sqdist)
        ret = np.array((dx, dy))
        return ret * (radsum / dist - 1)

    else:

        return np.array((0., 0.))


@dispatch(object, object)
def collidevector(a, b):

    raise NotImplementedError
