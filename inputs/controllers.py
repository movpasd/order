import numpy as np

from inputs.keyboard import controller, ControllerButton


@controller
class Paddle:

    north = ControllerButton("north")
    south = ControllerButton("south")
    east = ControllerButton("east")
    west = ControllerButton("west")

    def __init__(self, normalise=True):

        self.normalse = normalise
        self._norm = 1 / np.sqrt(2) if normalise else 1.0

        self.north = False
        self.south = False
        self.west = False
        self.east = False

    @north.set_keypress()
    def keypress_north(self):
        self.north = True

    @north.set_keyrelease()
    def keyrelease_north(self):
        self.north = False

    @south.set_keypress()
    def keypress_south(self):
        self.south = True

    @south.set_keyrelease()
    def keyrelease_south(self):
        self.south = False

    @east.set_keypress()
    def keypress_east(self):
        self.east = True

    @east.set_keyrelease()
    def keyrelease_east(self):
        self.east = False

    @west.set_keypress()
    def keypress_west(self):
        self.west = True

    @west.set_keyrelease()
    def keyrelease_west(self):
        self.west = False

    @property
    def x(self):

        n, s, e, w = self.north, self.south, self.east, self.west

        if not (e or w):
            return 0.0

        absv = self._norm if (n and not s) or (s and not n) else 1.0

        if e and not w:
            return absv
        if w and not e:
            return -absv

        return 0.0

    @property
    def y(self):

        n, s, e, w = self.north, self.south, self.east, self.west

        if not (n or s):
            return 0.0

        absv = self._norm if (e and not w) or (w and not e) else 1.0

        if n and not s:
            return absv
        if s and not n:
            return -absv

        return 0.0

    @property
    def vector(self):
        return np.array((self.x, self.y))
