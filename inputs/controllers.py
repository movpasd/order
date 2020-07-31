import numpy as np

from inputs.keyboard import controller, ControllerButton


@controller
class Paddle:

    north = ControllerButton("north")
    south = ControllerButton("south")
    east = ControllerButton("east")
    west = ControllerButton("west")

    def __init__(self, normalise=True):

        self.normalise = normalise
        self._norm = 1 / np.sqrt(2) if normalise else 1.0

        self.north = False
        self.south = False
        self.west = False
        self.east = False

    @north.set_keypress()
    def _(self):
        self.north = True

    @north.set_keyrelease()
    def _(self):
        self.north = False

    @south.set_keypress()
    def _(self):
        self.south = True

    @south.set_keyrelease()
    def _(self):
        self.south = False

    @east.set_keypress()
    def _(self):
        self.east = True

    @east.set_keyrelease()
    def _(self):
        self.east = False

    @west.set_keypress()
    def _(self):
        self.west = True

    @west.set_keyrelease()
    def _(self):
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


@controller
class Slider:

    decrease = ControllerButton("decrease")
    increase = ControllerButton("increase")

    def __init__(self):

        self.decrease = False
        self.increase = False

    @decrease.set_keypress()
    def _(self):
        self.decrease = True

    @decrease.set_keyrelease()
    def _(self):
        self.decrease = False

    @increase.set_keypress()
    def _(self):
        self.increase = True

    @increase.set_keyrelease()
    def _(self):
        self.increase = False

    @property
    def value(self):

        if self.decrease and not self.increase:
            return -1
        if self.increase and not self.decrease:
            return 1

        return 0


@controller
class Counter:

    increment = ControllerButton("increment")
    decrement = ControllerButton("decrement")

    def __init__(self, vinit=0, vmin=None, vmax=None):

        self.vmin = vmin
        self.vmax = vmax
        self._count = vinit

    @property
    def count(self):
        return self._count

    @increment.set_keypress()
    def _(self):

        if self.vmax is not None:
            if self.count >= self.vmax:
                return

        self._count += 1

    @decrement.set_keypress()
    def _(self):

        if self.vmin is not None:
            if self.count <= self.vmin:
                return

        self._count -= 1
