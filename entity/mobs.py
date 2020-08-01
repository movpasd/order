import numpy as np

from entity import Entity
import render.scenes as rsc
import utils.floatshapes as fs


class HasPosition:

    def __init__(self, x, y):
        self.pos = np.array((x, y), float)

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @y.setter
    def y(self, value):
        self.pos[1] = value


class Card:

    def __init__(self, surface, rect, h, alpha=None, visible=True):

        self.rect = rect
        self.surface = surface
        self.h = h
        self.alpha = alpha
        self.visible = visible

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect = self.rect.movedto(*value)

    def create_sprite(self):

        rect = self.rect.shifted(0, self.h)
        y = self.rect.cy

        return rsc.Sprite(self.surface, rect,
                          alpha=self.alpha, z=y,
                          visible=self.visible)


class EVisible(Entity, HasPosition):

    def __init__(self, cards, x, y, h, scale=1.0, visible=False):

        super().__init__()
        HasPosition.__init__(self, x, y)
        self.h = h
        self.scale = scale
        self.visible = visible

        self._cards = []
        self._sprites = {}

        for c in cards:
            self.add_card(c)

        self._move_sprites()

    @property
    def cards(self):
        return self._cards.copy()

    @property
    def sprites(self):
        return list(self._sprites.values())

    def add_card(self, card):

        self._cards.append(card)
        self._sprites[card] = card.create_sprite()
        self._move_sprites(ids=(-1,))

    def remove_card(self, card):

        self._cards.remove(card)
        del self._sprites[card]

    def _move_sprites(self, ids=None):

        if ids is None:
            ids = range(len(self._cards))

        sc = self.scale

        for i in ids:

            card = self._cards[i]
            sprite = self._sprites[card]

            relpos = self.pos + card.pos * sc
            relpos[1] += self.h + card.h
            w, h = card.rect.size

            sprite.rect = fs.FloatRect.from_center(*relpos, w * sc, h * sc)
            sprite.z = card.rect.cy

    def add_to_scene(self, scene):

        self.remove_from_scene(scene)
        scene.sprites.extend(self.sprites)

    def remove_from_scene(self, scene):

        for sprite in self.sprites:
            if sprite in scene.sprites:
                scene.sprites.remove(sprite)

    def tick(self, dt):

        self._move_sprites()
        super().tick(dt)


class MyMob(EVisible):

    def __init__(self, surface, x, y, h):

        rect1 = fs.FloatRect.from_center(0, 0, 1, 1)
        rect2 = fs.FloatRect.from_center(0, 1, 0.5, 0.5)

        card1 = Card(surface, rect1, 0)
        card2 = Card(surface, rect2, 0)

        super().__init__([card1, card2], x, y, h)

        self.sat = card2

    def tick(self, dt):

        c, s = np.cos(self.clock), np.sin(self.clock)
        rect = fs.FloatRect.from_center(c, s, 0.5, 0.5)

        self.sat.rect = rect

        super().tick(dt)

class MyMob2(EVisible):

    def __init__(self, surface, x, y, h):

        rect = fs.FloatRect.from_center(0, 0, 0.75, 0.75)
        card = Card(surface, rect, 0)

        super().__init__([card], x, y, h)

        self.card = card

    def tick(self, dt):

        c, s = np.cos(1.15*self.clock), np.sin(1.15*self.clock)
        rect = fs.FloatRect.from_center(0, c, 0.75, 0.75)

        self.card.rect = rect
        self.card.h = s

        super().tick(dt)