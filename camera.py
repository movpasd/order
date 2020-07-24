"""Module for rendering onto pygame Surface objects"""

from abc import ABC, abstractmethod

import numpy as np
import pygame.draw as pgdraw
from pygame import Rect

from utils import FloatRect


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Classes


class Sprite(ABC):

    def __init__(self, x, y, visible=True):

        self.pos = np.array((float(x), float(y)))
        self.visible = visible

    @abstractmethod
    def draw(self, screen, camera):
        pass

    @abstractmethod
    def in_frame(self, rect):
        """Check for intersection with a FloatRect"""
        pass

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @x.setter
    def x(self, val):
        self.pos[0] = val

    @y.setter
    def y(self, val):
        self.pos[1] = val


class SpriteShape(Sprite):

    def __init__(self, x, y, color=BLACK, thickness=0, visible=True):

        super().__init__(x, y, visible)
        self.color = color
        self.thickness = thickness


class SpriteCircle(SpriteShape):

    def __init__(self, x, y, radius, color=BLACK, thickness=0, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.radius = float(radius)

    def draw(self, screen, camera):

        pgdraw.circle(screen, self.color,
                           camera.px(self.pos),
                           camera.px(self.radius),
                           self.thickness)

    def in_frame(self, framerect):

        if not self.visible:
            return False

        if type(framerect) is Camera:
            framerect = framerect.get_framerect()

        x, y = self.pos
        r = self.radius

        halfwidth = framerect.width / 2
        halfheight = framerect.height / 2

        # Distance of circle to center of rectangle
        cdx = np.abs(x - framerect.centerx)
        cdy = np.abs(y - framerect.centery)

        if (cdx > halfwidth + r) or (cdy > halfheight + r):
            return False

        if (cdx <= halfwidth) or (cdy <= halfheight):
            return True

        # Distance of circle to rectangle corner
        sqcornerdist = (cdx - halfwidth)**2 + (cdy - halfheight)**2
        return sqcornerdist <= r**2


class SpriteRectangle(SpriteShape):

    def __init__(self, x, y, width, height, color=BLACK, thickness=0, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.width, self.height = float(width), float(height)

    def get_rect(self):
        """Get the bounding pygame Rect object"""
        x, y = self.pos
        return FloatRect(x - self.width / 2,
                         y + self.height / 2, self.width, self.height)

    def draw(self, screen, camera):

        pgdraw.rect(screen, self.color,
                         camera.px(self.get_rect()),
                         self.thickness)

    def in_frame(self, framerect):

        if not self.visible:
            return False

        if type(framerect) is Camera:
            return framerect

        return framerect.colliderect(self.get_rect())

    @classmethod
    def from_floatrect(cls, frect, **kw):

        return SpriteRectangle(frect.centerx, frect.centery,
                               frect.width, frect.height, **kw)


class SpriteGrid(SpriteShape):

    def __init__(self, x, y, spacing, color=BLACK,
                 thickness=1, boundrect=None, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.spacing = spacing
        self.boundrect = boundrect

    def draw(self, screen, camera):

        framerect = camera.get_framerect()
        brect = self.boundrect
        x0, y0 = self.pos
        sp = self.spacing

        bottom = np.maximum(framerect.bottom, brect.bottom)
        top = np.minimum(framerect.top, brect.top)
        left = np.maximum(framerect.left, brect.left)
        right = np.minimum(framerect.right, brect.right)

        deltax = -(left - x0) % sp
        deltay = -(bottom - y0) % sp

        for x in np.arange(deltax + left, right, sp):

            pgdraw.line(screen, self.color,
                             camera.px(x, bottom),
                             camera.px(x, top))

        for y in np.arange(deltay + bottom, top, sp):

            pgdraw.line(screen, self.color,
                             camera.px(left, y),
                             camera.px(right, y))

    def in_frame(self, framerect):

        if not self.visible:
            return False

        if type(framerect) is Camera:
            return framerect

        if self.boundrect is None:
            return True
        else:
            return framerect.colliderect(self.boundrect)


class SpriteImage(Sprite):

    def __init__(self, x, y, visible=True): pass


class Scene:

    def __init__(self, bg=WHITE, sprites=[]):

        self.bg = bg
        self.sprites = list(sprites)


class Camera:
    """Renders Scenes to pygame Surface"""

    def __init__(self, screen, scene, center=np.zeros(2), scale=25.0):

        self.screen = screen
        self.screensize = np.array(screen.get_size())

        self.scene = scene

        self.center = center
        self.scale = scale

    def px(self, p, q=None):
        """Convert scene coords to pixel coords"""

        if q is not None:
            p = (p, q)

        t = type(p)

        if t is int or t is float:
            return int(p * self.scale)

        if t is FloatRect:
            return Rect(
                self.px(p.topleft),
                (self.px(p.width), self.px(p.height))
            )

        p = np.array(p, dtype=float)
        p -= self.center
        p[1] = -p[1]

        r = self.screensize / 2 + self.scale * p

        return (int(r[0]), int(r[1]))

    def pos(self, pixels):
        """Convert pixel coords to scene coords"""

        t = type(pixels)
        if t is int or t is float:
            return pixels / self.scale

        pixels = np.array(pixels)
        pixels = pixels - screensize / 2
        pixels[1] = -pixels[1]

        return self.center + pixels / self.scale

    def to_length(self, pixels):

        return pixels / self.scale

    def draw(self):
        """Draw the scene onto the Camera's screen"""

        self.screen.fill(self.scene.bg)

        for sprite in self.scene.sprites:
            if sprite.in_frame(self.get_framerect()):
                sprite.draw(self.screen, self)

    def get_framerect(self):
        """Returns scene coords of camera view"""
        width, height = self.to_length(self.screensize)
        left = self.center[0] - width / 2
        top = self.center[1] + height / 2
        return FloatRect(left, top, width, height)

    def zoom(self, factor):
        self.scale *= factor

    def shift(self, delta):
        self.center += delta
