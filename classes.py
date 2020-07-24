"""General purpose utility classes"""

import numpy as np


def point(x, y=None):

    if y is None:
        return np.array(x)
    else:
        return np.array((x, y))


class FloatRect:
    """Rectangle class; treat as immutable"""

    def __init__(self, left, top, width, height):

        self._left = float(left)
        self._top = float(top)
        self._width = float(width)
        self._height = float(height)

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._top - self._height

    @property
    def right(self):
        return self._left + self._width

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def centerx(self):
        return self._left + self._width / 2

    @property
    def centery(self):
        return self._top - self._height / 2

    @property
    def center(self):
        return point(self.centerx, self.centery)

    @property
    def topleft(self):
        return point(self.top, self.left)

    @property
    def topright(self):
        return point(self.top, self.right)

    @property
    def bottomleft(self):
        return point(self.bottom, self.left)

    @property
    def bottomright(self):
        return point(self.bottom, self.right)

    def colliderect(self, other):

        # print(self.left, other.right)
        # print(self.right, other.left)
        # print(self.bottom, other.top)
        # print(self.top, other.bottom)
        # print()

        if (self.left > other.right or
                self.right < other.left or
                self.bottom > other.top or
                self.top < other.bottom):

            return False

        return True
