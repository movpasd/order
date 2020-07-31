import pygame as pg
import numpy as np
from collections import namedtuple
from warnings import warn

import render
import utils.floatshapes as fs


class Scene(render.Renderable):
    """Main class for organising rendering of 2D scenes"""

    def __init__(self, camera, bg=(255, 0, 255)):

        self._bg = bg
        self._camera = camera

        self.sprites = []

    @property
    def camera(self):
        return self._camera

    @property
    def bg(self):
        return self._bg

    def draw(self, screen):

        if screen.get_size() != self._camera.screensize:
            warn("screen size not compatible with camera; "
                 "there may be unexpected behaviour")

        screen.fill(self._bg)

        cam = self.camera

        self.sprites.sort(key=lambda s: s.z)
        blits = [(sprite.get_resized_surface(cam),
                  cam.px_point(sprite.get_bounding_rect().topleft))
                 for sprite in self.sprites
                 if sprite.visible and cam.inframe(sprite.rect)]
        screen.blits(blit_sequence=blits)


class Camera:
    """Stores information on scaling and positioning of Scenes"""

    def __init__(self, screensize, scale=1.0, center=None):

        self.screensize = screensize
        self.scale = float(scale)

        if center is None:
            self.center = np.array((0., 0.))
        else:
            self.center = np.array(center, float)

    # Properties

    @property
    def frame(self):
        w, h = self.px_size(self.screensize)
        return fs.FloatRect.from_center(*self.center, w, h)

    # Methods

    def inframe(self, frect):
        return self.frame.colliderect(frect)

    def px_inframe(self, pgrect):
        return pgrect.colliderect(pg.Rect((0, 0), self.screensize))

    # Conversion Methods

    def px_point(self, point):

        point = np.array(point, float)

        newpoint = (point - self.center) * self.scale
        return (self.screensize[0] / 2 + int(newpoint[0]),
                self.screensize[1] / 2 - int(newpoint[1]))

    def px_length(self, length):
        return int(length * self.scale)

    def px_size(self, size):
        return (self.px_length(size[0]), self.px_length(size[1]))

    def px_rect(self, frect):
        return pg.Rect(self.px_point(frect.topleft),
                       self.px_size(frect.size))

    #

    def pos_point(self, point):

        newpoint = np.array((point[0] - self.screensize[0] / 2,
                             self.screensize[1] / 2 - point[1]))

        return self.center + newpoint / self.scale

    def pos_length(self, length):
        return length / self.scale

    def pos_size(self, size):
        return (self.pos_length(size[0]), self.pos_length(size[1]))

    def pos_rect(self, pgrect):
        return FloatRect(*self.pos_point(pgrect.bottomleft),
                         self.pos_size(pgrect.size))


class Sprite:
    """
    Basic movable, scalable, rotatable screen element

    Has basic caching to avoid scaling and 
    """

    def __init__(self, surface, rect, alpha=None, z=0.0, angle=0, visible=True):

        self.rect = rect
        self.surface = surface
        self.z = z
        self.angle = angle
        self.visible = visible
        self.alpha = alpha

        self._pointer_prev_surface = surface
        self._cached_surface = None
        self._cached_scale = None
        self._cached_angle = None

    @property
    def pos(self):
        return self.rect.center

    @property
    def x(self):
        return self.rect.cx

    @property
    def y(self):
        return self.rect.cy

    @pos.setter
    def pos(self, value):
        self.rect = self.rect.movedto(*value)

    @x.setter
    def x(self, value):
        self.rect = self.rect.movedto(value, None)

    @y.setter
    def y(self, value):
        self.rect = self.rect.movedto(None, value)

    # Methods

    def get_bounding_rect(self):
        """
        returns rectangle which fully contains Sprite;
        if angle = 0 this is equivalent to the sprite's rect
        """

        rect = self.rect

        if self.angle == 0:
            return rect
        else:
            return rect.rotated_bounds(self.angle)


    def get_resized_surface(self, camera, update=True):

        if update:
            self._update_cached(camera)

        return self._cached_surface

    def _update_cached(self, camera, force=False):

        sf, angle, alpha = self.surface, self.angle, self.alpha

        if not force and (self._pointer_prev_surface == sf and
                          self._cached_angle == angle and
                          self._cached_scale == camera.scale):
            return  # if surface nor angle changed and scale is still
            # compatible with camera, no need to update

        pxsize = camera.px_size(self.rect.size)
        self._cached_surface = pg.transform.scale(sf, pxsize)

        if angle != 0:
            self._cached_surface = pg.transform.rotate(
                self._cached_surface, angle)

        if alpha is not None:
            self._cached_surface.set_alpha(alpha)

    # Constructors

    @classmethod
    def from_imgpath(self, imgpath, rect, z=0.0, angle=0, visible=True):

        surf = pg.image.load(str(imgpath))
        surf.convert()

        return Sprite(surf, rect, z=z, angle=angle, visible=visible)


class SpriteCircle(Sprite):

    def __init__(self, color, rect, alpha=None, z=0.0, angle=0, visible=True):

        super().__init__(None, rect, alpha=alpha, z=z, angle=angle, visible=visible)
        self.color = color

    def _update_cached(self, camera, force=False):

        angle, alpha = self.angle, self.alpha

        if not force and (self._cached_angle == angle and
                          self._cached_scale == camera.scale):
            return  # if surface nor angle changed and scale is still
            # compatible with camera, no need to update

        pxsize = camera.px_size(self.rect.size)
        sf = pg.Surface(pxsize)

        if self.color == (0, 0, 0):
            sf.fill((255, 255, 255))
            sf.set_colorkey((255, 255, 255))
        else:
            sf.set_colorkey((0, 0, 0))

        pg.draw.ellipse(sf, self.color, pg.Rect((0, 0), pxsize))

        pxsize = camera.px_size(self.rect.size)
        self._cached_surface = pg.transform.scale(sf, pxsize)

        if angle != 0:
            self._cached_surface = pg.transform.rotate(
                self._cached_surface, angle)

        if alpha is not None:
            self._cached_surface.set_alpha(alpha)
