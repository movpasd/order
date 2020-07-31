import numpy as np


FACING_XY = "xy"
FACING_YZ = "yz"
FACING_ZX = "zx"


class Float3DCuboid:
    """Cuboid class; treat as immutable"""

    def __init__(self, left, bottom, back, width, height, depth):

        self._left = float(left)
        self._bottom = float(bottom)
        self._back = float(back)
        self._width = float(width)
        self._height = float(height)
        self._depth = float(depth)

    @property
    def left(self):
        return self._left

    @property
    def bottom(self):
        return self._bottom

    @property
    def back(self):
        return self._back

    @property
    def right(self):
        return self._left + self._width

    @property
    def top(self):
        return self._bottom + self._height

    @property
    def front(self):
        return self._back + self._depth

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def depth(self):
        return self._depth

    @property
    def centerx(self):
        return (self._left + self._right) / 2

    @property
    def centery(self):
        return (self._bottom + self._top) / 2

    @property
    def centerz(self):
        return (self._back + self._front) / 2

    @property
    def center(self):
        return np.array(self.centerx, self.centery, self.centerz)

    def collidecuboid(self, other, strict=True):

        if strict:

            return not (self.left >= other.right or
                        self.right <= other.left or
                        self.bottom >= other.top or
                        self.top <= other.bottom or
                        self.back >= other.front or
                        self.front <= other.back)
        else:

            return not (self.left > other.right or
                        self.right < other.left or
                        self.bottom > other.top or
                        self.top < other.bottom or
                        self.back > other.front or
                        self.front < other.back)

    @classmethod
    def from_center(cls, cx, cy, cz, width, height, depth):

        return cls(
            cx - width / 2,
            cy - height / 2,
            cz - depth / 2,
            width, height, depth
        )
