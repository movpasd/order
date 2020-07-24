"""Handles keyboard & mouse inputs for pygame"""

# TODO: add modded key support -- it has to be optional in a sense

import pygame as pg
import numpy as np

from abc import ABC, abstractmethod
from collections import namedtuple


KeyCombo = namedtuple("KeyCombo", ["key", "state"])
# ModdedKeyCombo = namedtuple("ModdedKeyCombo", ["key", "mod", "state"])


KSTATE_DOWN = "down"
KSTATE_UP = "up"


class KeyTrigger(ABC):

    @abstractmethod
    def bind(self, dispatcher, *args):
        pass


class KeyStateTrigger(KeyTrigger):
    """Base class/interface for objects that respond to key presses"""

    @abstractmethod
    def on_trigger(self, action):
        pass


class Paddle(KeyStateTrigger):
    """
    Simulates a joystick with 8 directional settings

    Actions: L_on, L_on, R_on, R_on, U_on, U_on, Du, Dd
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

        if action == "L_off":
            self.L = False
        elif action == "L_on":
            self.L = True
        elif action == "R_off":
            self.R = False
        elif action == "R_on":
            self.R = True
        elif action == "U_off":
            self.U = False
        elif action == "U_on":
            self.U = True
        elif action == "D_off":
            self.D = False
        elif action == "D_on":
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

        dispatcher.bind(KeyCombo(left, KSTATE_UP), self, "L_off")
        dispatcher.bind(KeyCombo(left, KSTATE_DOWN), self, "L_on")
        dispatcher.bind(KeyCombo(right, KSTATE_UP), self, "R_off")
        dispatcher.bind(KeyCombo(right, KSTATE_DOWN), self, "R_on")
        dispatcher.bind(KeyCombo(up, KSTATE_UP), self, "U_off")
        dispatcher.bind(KeyCombo(up, KSTATE_DOWN), self, "U_on")
        dispatcher.bind(KeyCombo(down, KSTATE_UP), self, "D_off")
        dispatcher.bind(KeyCombo(down, KSTATE_DOWN), self, "D_on")


class Counter(KeyStateTrigger):

    def __init__(self, init=0, mincount=None, maxcount=None):

        if (
            (maxcount is not None and init > maxcount) or
            (mincount is not None and init < mincount)
        ):
            raise ValueError("init value is out of given bounds")

        self.count = init
        self.maxcount = maxcount
        self.mincount = mincount

    def on_trigger(self, action):

        if action == "increment":

            if self.maxcount is None or self.count < self.maxcount:
                self.count += 1

        elif action == "decrement":

            if self.mincount is None or self.count > self.mincount:
                self.count -= 1

    def bind(self, dispatcher, increment, decrement):
        """
        Binds keys to modify counter

        dispatcher: KeyDispatcher
        left, right, up, down: pygame.key.K_ constants

        The same modifier is applied to the whole paddle.
        """

        dispatcher.bind(KeyCombo(increment, KSTATE_DOWN), self, "increment")
        dispatcher.bind(KeyCombo(decrement, KSTATE_DOWN), self, "decrement")


class KeyDispatcher:
    """
    Used to dispatch key events to pre-registered triggers
    bound to specific key combos

    For up/down triggers, the dispatch() key must be called for
        each key up/key down event
    For held keys, the trigger_held() should be called every frame
    """

    def __init__(self):

        self.keystatetriggers = {}

    def bind(self, keycombo, keytrigger, action):

        self.keystatetriggers.setdefault(keycombo, [])
        self.keystatetriggers[keycombo].append((keytrigger, action))

    def unbind(self, keycombo):

        if keycombo in self.keystatetriggers:
            del self.keystatetriggers[keycombo]

    def unbindall(self):

        self.keystatetriggers = {}

    def trigger(self, keycombo):

        if keycombo in self.keystatetriggers:
            for keytrigger, action in self.keystatetriggers[keycombo]:
                keytrigger.on_trigger(action)

    def dispatch(self, event):

        if event.type == pg.KEYDOWN:
            keycombo = KeyCombo(event.key, KSTATE_DOWN)
        elif event.type == pg.KEYUP:
            keycombo = KeyCombo(event.key, KSTATE_UP)

        self.trigger(keycombo)
