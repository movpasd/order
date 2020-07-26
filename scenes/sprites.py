import numpy as np
import pygame.draw as pgdraw
from abc import ABC, abstractmethod

from scenes.camera import Camera

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Scene:

    def __init__(self, bg=WHITE, sprites=[]):

        self.bg = bg
        self.sprites = list(sprites)

    def add_sprite(self, sprite): self.sprites.append(sprite)

    def remove_sprite(self, sprite): self.sprites.remove(sprite)

    def clear(self): self.sprites = []


class Sprite(ABC):

    def __init__(self, x, y, visible=True):

        self.pos = np.array((float(x), float(y)))
        self.visible = visible

    def hide(self): self.visible = False

    def show(self): self.visible = True

    @abstractmethod
    def draw(self, screen, camera):
        pass

    @abstractmethod
    def in_frame(self, rect):
        """Check for intersection with a FloatRect"""
        pass

    @property
    def x(self): return self.pos[0]

    @property
    def y(self): return self.pos[1]

    @x.setter
    def x(self, val): self.pos[0] = val

    @y.setter
    def y(self, val):  self.pos[1] = val


class SpriteShape(Sprite):

    def __init__(self, x, y, color=BLACK, thickness=None, visible=True):

        super().__init__(x, y, visible)
        self.color = color
        self.thickness = thickness


class SpriteCircle(SpriteShape):

    def __init__(self, x, y, radius, color=BLACK, thickness=None, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.radius = float(radius)

    def draw(self, screen, camera):

        if self.thickness is None:
            px_thickness = 0
        elif self.thickness == 0:
            px_thickness = 1
        else:
            px_thickness = camera.px(self.thickness)

        pgdraw.circle(screen, self.color,
                      camera.px(self.pos),
                      camera.px(self.radius),
                      px_thickness)

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

    def __init__(self, x, y, width, height, color=BLACK, thickness=None, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.width, self.height = float(width), float(height)

    def get_rect(self):
        """Get the bounding pygame Rect object"""
        x, y = self.pos
        return FloatRect(x - self.width / 2,
                         y + self.height / 2, self.width, self.height)

    def draw(self, screen, camera):

        if self.thickness is None:
            px_thickness = 0
        elif self.thickness == 0:
            px_thickness = 1
        else:
            px_thickness = camera.px(self.thickness)

        pgdraw.rect(screen, self.color,
                    camera.px(self.get_rect()),
                    px_thickness)

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
                 thickness=None, boundrect=None, visible=True):

        super().__init__(x, y, color, thickness, visible)
        self.spacing = spacing
        self.boundrect = boundrect

    def draw(self, screen, camera):

        framerect = camera.get_framerect()
        brect = self.boundrect
        x0, y0 = self.pos
        sp = self.spacing

        if self.thickness is None:
            px_thickness = 1
        else:
            px_thickness = camera.px(self.thickness)

        if brect is not None:

            bottom = np.maximum(framerect.bottom, brect.bottom)
            top = np.minimum(framerect.top, brect.top)
            left = np.maximum(framerect.left, brect.left)
            right = np.minimum(framerect.right, brect.right)

        else:

            bottom = framerect.bottom
            top = framerect.top
            left = framerect.left
            right = framerect.right

        deltax = -(left - x0) % sp
        deltay = -(bottom - y0) % sp

        for x in np.arange(deltax + left, right, sp):

            pgdraw.line(screen, self.color,
                        camera.px(x, bottom),
                        camera.px(x, top),
                        px_thickness)

        for y in np.arange(deltay + bottom, top, sp):

            pgdraw.line(screen, self.color,
                        camera.px(left, y),
                        camera.px(right, y),
                        px_thickness)

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
