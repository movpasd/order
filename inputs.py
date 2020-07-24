"""Handles keyboard & mouse inputs for pygame"""

import pygame as pg
import numpy as np

from abc import ABC, abstractmethod
from collections import namedtuple


KeyCombo = namedtuple("KeyCombo", ["key", "state"])
# ModdedKeyCombo = namedtuple("ModdedKeyCombo", ["key", "mod", "state"])
# TODO: Add modded key combinations

KSTATE_HELD = "held"
KSTATE_DOWN = "down"
KSTATE_UP = "up"


class KeyTrigger(ABC):
    """Base class/interface for objects that respond to key presses"""

    @abstractmethod
    def on_trigger(self, action):
        pass

    @abstractmethod
    def bind(self, dispatcher, *args):
        """
        Ease of use function for quickly binding actions to dispatcher

        dispatcher: KeyDispatcher
        bindings: dict : action -> keycombo
        """

        pass


class Paddle(KeyTrigger):
    """
    Simulates a joystick with 8 directional settings

    Actions: Lu, Ld, Ru, Rd, Uu, Ud, Du, Dd
    """

    def __init__(self, norm_diag=True):

        self.L = False
        self.R = False
        self.U = False
        self.D = False

        if norm_diag:
            self.norm = 1 / np.sqrt(2)
        else:
            self.norm = 1

    def on_trigger(self, action):

        if action == "Lu":
            self.L = False
        elif action == "Ld":
            self.L = True
        elif action == "Ru":
            self.R = False
        elif action == "Rd":
            self.R = True
        elif action == "Uu":
            self.U = False
        elif action == "Ud":
            self.U = True
        elif action == "Du":
            self.D = False
        elif action == "Dd":
            self.D = True

    @property
    def x(self):

        l, r, u, d = self.L, self.R, self.U, self.D

        if (not l and not r) or (l and r):
            return 0.0

        norm = self.norm if (u or d) else 1.0

        if l and not r:
            return -norm
        if not l and r:
            return norm

    @property
    def y(self):

        l, r, u, d = self.L, self.R, self.U, self.D

        if (not u and not d) or (u and d):
            return 0.0

        norm = self.norm if (l or r) else 1.0

        if u and not d:
            return norm
        if not u and d:
            return -norm

    @property
    def vector(self):
        return np.array((self.x, self.y))
    

    def bind(self, dispatcher, left, right, up, down):
        """
        Binds paddle keys within a KeyDispacher

        dispatcher: KeyDispatcher
        left, right, up, down: pygame.key.K_ constants

        The same modifier is applied to the whole paddle.
        """

        dispatcher.bind(KeyCombo(left, KSTATE_UP), self, "Lu")
        dispatcher.bind(KeyCombo(left, KSTATE_DOWN), self, "Ld")
        dispatcher.bind(KeyCombo(right, KSTATE_UP), self, "Ru")
        dispatcher.bind(KeyCombo(right, KSTATE_DOWN), self, "Rd")
        dispatcher.bind(KeyCombo(up, KSTATE_UP), self, "Uu")
        dispatcher.bind(KeyCombo(up, KSTATE_DOWN), self, "Ud")
        dispatcher.bind(KeyCombo(down, KSTATE_UP), self, "Du")
        dispatcher.bind(KeyCombo(down, KSTATE_DOWN), self, "Dd")


class KeyDispatcher:
    """
    Used to dispatch key events to pre-registered triggers
    bound to specific key combos

    For up/down triggers, the dispatch() key must be called for
        each key up/key down event
    For held keys, the trigger_held() should be called every frame
    """

    def __init__(self):

        self.triggers = {}
        self._held_triggers = []

    def bind(self, keycombo, keytrigger, action):

        self.triggers.setdefault(keycombo, [])
        self.triggers[keycombo].append((keytrigger, action))

        if keycombo.state == KSTATE_HELD:
            self._held_triggers.append(keycombo)

    def unbind(self, keycombo):

        if keycombo in self.triggers:
            del self.triggers[keycombo]

        if keycombo in self._held_triggers:
            self._held_triggers.remove(keycombo)

    def unbindall(self):

        self.triggers = {}
        self._held_triggers = []

    def trigger(self, keycombo):

        if keycombo in self.triggers:
            for keytrigger, action in self.triggers[keycombo]:
                keytrigger.on_trigger(action)

    def dispatch(self, event):

        if event.type == pg.KEYDOWN:
            keycombo = KeyCombo(event.key, KSTATE_DOWN)
        elif event.type == pg.KEYUP:
            keycombo = KeyCombo(event.key, KSTATE_UP)

        self.trigger(keycombo)

    def trigger_held(self):

        pressed = pg.key.get_pressed()

        for keycombo in self._held_triggers:
            if pressed[keycombo.key]:
                self.trigger(keycombo)
