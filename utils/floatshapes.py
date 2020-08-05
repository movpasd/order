"""General purpose utility classes"""

import numpy as np


_DEG2RAD = np.pi / 180


def toarray(x, y=None):
    """converts to numpy array"""

    if y is None:
        return np.array(x)
    else:
        return np.array((x, y))


def rotate(point, angle, about=(0, 0)):
    """rotates 'point' by 'angle' about 'about'"""

    angle *= _DEG2RAD

    ax, ay = about
    dx, dy = point[0] - ax, point[1] - ay
    c, s = np.cos(angle), np.sin(angle)

    return toarray(ax + c * dx - s * dy,
                   ay + s * dx + c * dy)


class FloatRect:
    """Rectangle class; treat as immutable"""

    def __init__(self, left, bottom, width, height):

        if width < 0 or height < 0:
            raise ValueError("width and height must be positive")

        self._left = float(left)
        self._bottom = float(bottom)
        self._width = float(width)
        self._height = float(height)

    # Basic properties

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._bottom + self._height

    @property
    def bottom(self):
        return self._bottom

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
    def size(self):
        return (self.width, self.height)

    @property
    def centerx(self):
        return self._left + self._width / 2

    @property
    def cx(self):
        return self._left + self._width / 2

    @property
    def centery(self):
        return self._bottom + self._height / 2

    @property
    def cy(self):
        return self._bottom + self._height / 2

    @property
    def center(self):
        return toarray(self.centerx, self.centery)

    @property
    def topleft(self):
        return toarray(self.left, self.top)

    @property
    def topright(self):
        return toarray(self.right, self.top)

    @property
    def bottomleft(self):
        return toarray(self.left, self.bottom)

    @property
    def bottomright(self):
        return toarray(self.right, self.bottom)

    @property
    def corners(self):
        return [self.bottomleft, self.bottomright,
                self.topright, self.topleft]

    @property
    def relative_corners(self):
        hw, hh = self.width / 2, self.height / 2
        return [toarray(hw, hh), toarray(hw, -hh),
                toarray(-hw, hh), toarray(-hw, -hh)]

    # Dunders

    def __eq__(self, other):
        return (self._left == other._left and
                self._bottom == other._bottom and
                self._width == other._width and
                self._height == other._height)

    def __hash__(self):
        return hash((self._left, self._bottom, self._width, self._height))

    # Moving methods

    def shifted(self, dx, dy):
        return FloatRect(self.left + dx, self.bottom + dy,
                         self.width, self.height)

    def movedto(self, newx, newy):

        newx = newx or self.cx
        newy = newy or self.cy

        return FloatRect.from_center(newx, newy, self.width, self.height)

    def resized(self, newwidth, newheight, scalefrom="center"):

        nw = newwidth or self.width
        nh = newheight or self.height

        if scalefrom == "center":
            return FloatRect.from_center(self.cx, self.cy, nw, nh)

        if scalefrom == "bottomleft":
            return FloatRect(self.left, self.bottom, nw, nh)

        if scalefrom == "bottomright":
            return FloatRect(self.right - nw, self.bottom, nw, nh)

        if scalefrom == "topleft":
            return FloatRect(self.left, self.top - nh, nw, nh)

        if scalefrom == "topright":
            return FloatRect(self.right - nw, self.top - nh, nw, nh)

    def scaled(self, scale, scalefrom="center"):
        return self.resized(self.width * scale, self.height * scale,
                            scalefrom=scalefrom)

    def xyscaled(self, scalex, scaley, scalefrom="center"):
        return self.resized(self.width * scalex, self.height * scaley,
                            scalefrom=scalefrom)

    def expanded(self, expandx, expandy):
        return FloatRect.from_center(self.cx, self.cy,
                                     self.width + expandx,
                                     self.height + expandy)

    def rotated_bounds(self, angle):
        """Bounding axis-aligned rectangle of rotated rectangle"""

        return FloatRect.that_contains([rotate(p, angle, self.center)
                                        for p in self.corners])

    def rotated90(self):
        return FloatRect.from_center(self.cx, self.cy,
                                     self.height, self.width)

    # Other methods

    def colliderect(self, other, strict=True):

        if strict:

            return not (self.left >= other.right or
                        self.right <= other.left or
                        self.bottom >= other.top or
                        self.top <= other.bottom)

        else:

            return not (self.left > other.right or
                        self.right < other.left or
                        self.bottom > other.top or
                        self.top < other.bottom)

    def intersectrect(self, other):

        if self.colliderect(other, strict=False):

            left = np.amax((self.left, other.left))
            right = np.amin((self.right, other.right))
            bottom = np.amax((self.bottom, other.bottom))
            top = np.amin(self.right, other.right)

            return FloatRect.from_sides(left, right, bottom, top)

        return None

    # Constructors

    @classmethod
    def from_center(cls, cx, cy, width, height):
        """rectangle defined by center coords and size"""
        return cls(cx - width / 2, cy - height / 2, width, height)

    @classmethod
    def from_sides(cls, left, right, bottom, top, strictsigns=True):
        """rectangle defined by coords of sides"""

        if left > right or bottom > top:

            if strictsigns:
                raise ValueError("left can't be greater than right "
                                 "nor bottom greater than top")

            left, right = right, left
            bottom, top = top, bottom

        return cls(left, bottom, right - left, top - bottom)

    @classmethod
    def from_corners(cls, p1, p2):
        """rectangle from opposing corners"""
        return cls.that_contains([p1, p2])

    @classmethod
    def that_contains(cls, points):
        """smallest rectangle that all points in given list"""

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        left = np.amin(xs)
        right = np.amax(xs)
        bottom = np.amin(ys)
        top = np.amax(ys)

        return cls.from_sides(left, right, bottom, top)


class FloatCircle:

    def __init__(self, centerx, centery, radius):

        self._cx = centerx
        self._cy = centery
        self._radius = radius

    @property
    def center(self):
        return toarray(self._cx, self._cy)

    @property
    def centerx(self):
        return self._cx

    @property
    def centery(self):
        return self._cy

    @property
    def cx(self):
        return self._cx

    @property
    def cy(self):
        return self._cy

    @property
    def radius(self):
        return self._radius

    @property
    def r(self):
        return self._radius

    @property
    def diameter(self):
        return 2 * self._radius

    def shifted(self, dx, dy):
        return FloatCircle(self.cx + dx, self.cy + dy,
                           self.radius)

    def get_rect(self):
        w = self.diameter
        return FloatRect.from_center(self.cx, self.cy, w, w)
