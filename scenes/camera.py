"""Module for rendering onto pygame Surface objects"""

import numpy as np
import pygame.draw as pgdraw
from pygame import Rect

from utils import FloatRect


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
