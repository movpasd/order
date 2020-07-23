import numpy as np
import pygame
from pygame import Surface, Rect


# Classes

class Sprite:

    def __init__(self, x=0, y=0):
        self.pos = np.array((float(x), float(y)))

    def draw(self, screen, camera):
        pass

    def intersects(self, rect):
        """Check for intersection with a pygame Rect"""
        pass


class ShapeSprite(Sprite):

    def __init__(self, x=0, y=0, color=(255, 255, 255)):

        super().__init__(x, y)
        self.color = color


class Circle(ShapeSprite):

    def __init__(self, x=0, y=0, radius=1.0, color=(255, 255, 255)):

        super().__init__(x, y, color)
        self.radius = float(radius)

    def draw(self, screen, camera):

        cx, cy = camera.to_pixels(self.pos)
        pygame.draw.circle(screen, self.color,
                           camera.to_pixels(self.pos),
                           camera.to_pixels(self.radius))

    def intersects(self, rect):

        x, y = self.pos
        r = self.radius

        halfwidth = rect.width / 2
        halfheight = rect.height / 2

        # Distance of circle to center of rectangle
        print(rect.centery)
        cdx = np.abs(x - rect.centerx)
        cdy = np.abs(y - rect.centery)

        if (cdx > halfwidth + r) or (cdy > halfheight + r):
            return False

        if (cdx <= halfwidth) and (cdy <= halfheight):
            return True

        # Distance of circle to rectangle corner
        sqcornerdist = (cdx - halfwidth)**2 + (cdy - halfheight)**2
        return sqcornerdist <= r**2


class Scene:

    def __init__(self, bg=(0, 0, 0), sprites=[]):

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

    def to_pixels(self, pos):
        """Convert scene coords to pixel coords"""

        t = type(pos)
        if t is int or t is float:
            return int(pos * self.scale)

        pos = np.array(pos)
        pos -= self.center
        pos[1] = -pos[1]

        r = self.screensize / 2 + self.scale * pos

        return (int(r[0]), int(r[1]))

    def to_pos(self, pixels):
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
            if sprite.intersects(self.get_rect()):
                sprite.draw(self.screen, self)

    def get_rect(self):
        """Returns scene coords of camera view"""
        width, height = self.to_length(self.screensize)
        left = self.center[0] - width / 2
        top = self.center[1] - height / 2
        return Rect(left, top, width, height)

    def zoom(self, factor):
        self.scale *= factor

    def shift(self, delta):
        self.center += delta
