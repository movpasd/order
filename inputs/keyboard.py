import pygame as pg
import inspect
from collections import namedtuple


KeyEvent = namedtuple("KeyEvent", ["key", "mod", "state"])
KeyBind = namedtuple("KeyBind", ["key", "mod"])

KSTATE_PRESS = 1
KSTATE_RELEASE = 0


class ControllerButton:

    def __init__(self, name):

        self.name = name
        self._on_keypress_func = None
        self._on_keyrelease_func = None

    def on_keypress(self, action, overwrite=False):

        if type(action) is not str:
            raise TypeError(f"action must be a str, not {type(action)}")

        def _decorator(func):

            if len(inspect.signature(func).parameters) != 1:
                raise TypeError(f"{func.__name__} has bad signature; "
                                "should be func(self)")

            if not overwrite:
                if self._on_keypress_func is not None:
                    raise ValueError(f"{action}'s' on_keypress already defined. "
                                     "Try setting overwrite=True?")

            self._on_keypress_func = func

            return func

        return _decorator

    def on_keyrelease(self, action, overwrite=False):

        if type(action) is not str:
            raise TypeError(f"action must be a str, not {type(action)}")

        def _decorator(func):

            if len(inspect.signature(func).parameters) != 1:
                raise TypeError(f"{func.__name__} has bad signature; "
                                "should be func(self)")

            if not overwrite:
                if self._on_keyrelease_func is not None:
                    raise ValueError(f"{action}'s' on_keyrelease already defined. "
                                     "Try setting overwrite=True?")

            self._on_keyrelease_func = func

            return func

        return _decorator


def controller(cls):
    """
    Decorator to create controller classes

    Makes it easy to create classes that respond to a specific key, both
    press and release, see e.g.: Paddle, Counter in controllers.py for
    examples of usage

    Each action can have a keypress and a keyrelease associated function
    """

    cls._kd_actions = {}  # : dict(str -> ControllerButton)

    for _, act_obj in inspect.getmembers(cls):
        if type(act_obj) is ControllerButton:
            cls._kd_actions[act_obj.name] = act_obj

    def _bind(self, keydispatcher, bindings, strict=True, rebind=False):
        """
        Bind a controller to a keydispatcher

        keydispatcher: KeyDispatcher
        bindings: dict (str -> pygame K_), gives KeyEvents to bind to each action name
        strict: bool. If true, checks that all names in bindings correspond to a
                    registered name, and checks that all actions have been bound
        rebind: bool. Passed onto keydispatched.bind(..)
        """

        if strict:

            for name in bindings:
                if name not in cls._kd_actions:
                    raise ValueError(f"{name} is not an action of {cls.__name__}")

            for name in cls._kd_actions:
                if name not in bindings:
                    raise ValueError(f"{name} is missing from bindings")

        for name, keybind in bindings.items():

            if type(keybind) is int:
                keybind = KeyBind(keybind, None)

            act_obj = cls._kd_actions[name]
            on_kp = act_obj._on_keypress_func
            on_kr = act_obj._on_keyrelease_func

            if on_kp is not None:

                ke = KeyEvent(*keybind, KSTATE_PRESS)
                keydispatcher.bind(ke, on_kp, args=(self,), rebind=rebind)

            if on_kr is not None:

                ke = KeyEvent(*keybind, KSTATE_RELEASE)
                keydispatcher.bind(ke, on_kr, args=(self,), rebind=rebind)

    cls.bind = _bind

    return cls


class KeyDispatcher:
    """
    Dispatches pygame keyboard events to functions

    The KeyDispatcher object stores a list of bindings as a dictionary mapping
    KeyBinding instances to functions.

    You can bind exactly one function to every KeyEvent.

    In terms of types, KeyEvent: (pygame K_, pygame KMOD_ or None, KSTATE_)
    so strictly speaking (int, int or None, int).
    """

    def __init__(self):

        self.bindings = {}

    def bind(self, keyevent, func, args=None, kwargs=None, rebind=False):
        """
        Create new binding to a function

        If keyevent.mod is None, the binding triggers for any press of the
        associated keyevent.key, regardless of mod.

        If you want the binding to trigger for no mod values, set mod=0.

        keyevent: KeyEvent to bind
        func: callable to bind to
        args, kwargs: tuple and dict to pass onto func on call
        rebind: bool. set to True if you want to overwrite a binding
        """

        if type(keyevent) is not KeyEvent:
            raise TypeError("keyevent should be of type KeyEvent")

        if not rebind and keyevent in self.bindings:
            raise ValueError(f"binding for {keyevent} already exists. "
                             "try passing rebind=True?")

        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}

        self.bindings[keyevent] = (func, args, kwargs)

    def unbind(self, keyevent):
        """Removes any binding of a keyevent to a function"""

        if keyevent in self.bindings:
            del self.bindings[keyevent]

    def trigger(self, keyevent):
        pass

    def dispatch(self, event):
        """
        Call this for every KEYDOWN and KEYUP event

        returne False if event isn't of the right type,
            True otherwise
        """

        if event.type == pg.KEYDOWN:
            ke_mod = KeyEvent(event.key, event.mod, KSTATE_PRESS)
            ke_nomod = KeyEvent(event.key, None, KSTATE_PRESS)
        elif event.type == pg.KEYUP:
            ke_mod = KeyEvent(event.key, event.mod, KSTATE_RELEASE)
            ke_nomod = KeyEvent(event.key, None, KSTATE_RELEASE)
        else:
            return False

        bs = self.bindings

        if ke_mod in bs:
            f, args, kwargs = bs[ke_mod]
            f(*args, **kwargs)

        if ke_nomod in bs:
            f, args, kwargs = bs[ke_nomod]
            f(*args, **kwargs)

        return True
