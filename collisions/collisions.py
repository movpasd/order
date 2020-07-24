"""Module for resolving 2D collisions"""

import inspect
from abc import ABC
import numpy as np


# A problem that arises when dealing with collisions between different types
# of objects is how to implement the double dispatch required. The function
# which computes the collision is different depending on the types of the
# hitboxes involved.
#
# It would be inelegant to implement this as a Hitbox.collide_with(..) method,
# as any addition of a Hitbox type would require going through every other
# Hitbox type to update the function.
#
# I instead opt for a solution by keeping track of Hitbox types in the module
# globals. Anytime I add a Hitbox type, I also must write collider functions
# and add these to the colliders.


hitbox_types = []
colliders = {}


def _collider_default(a, b):
    """The default collider function"""

    raise NotImplementedError(
        f"no collider defined between {type(a)} and {type(b)}"
    )


def new_hitbox_type(new_hitbox_type):

    global hitbox_types
    global colliders

    # Validation

    if not inspect.isclass(new_hitbox_type):
        raise ValueError(f"{new_hitbox_type} is not a class!")

    if not issubclass(new_hitbox_type, Hitbox):
        raise ValueError(f"{new_hitbox_type} does not extend Hitbox")

    # Actual function

    n = len(hitbox_types)

    hitbox_types.append(new_hitbox_type)

    for i, _ in enumerate(hitbox_types):
        colliders[(i, n)] = _collider_default
        colliders[(n, i)] = _collider_default


def set_collider(a, b, func):
    """
    Set the collider function between Hitbox types a and b

    func should have the signature:
    func : (obj1: a, obj2: b -> delta: (2,)-float array)
    It should output how much obj1 should move if obj2 is static
    """

    global hitbox_types
    global colliders

    # Validation

    if type(a) is not int:

        if not inspect.isclass(a):
            raise ValueError(f"{a} is not a class!")

        if not issubclass(a, Hitbox):
            raise ValueError(f"{a} does not extend Hitbox")

        if a not in hitbox_types:
            raise ValueError(
                f"{type(a)} not registered with collisions.py. "
                f"try calling new_hitbox_type({type(a)})"
            )
        else:
            a = hitbox_types.index(a)

    if type(b) is not int:

        if not inspect.isclass(b):
            raise ValueError(f"{b} is not a class!")

        if not issubclass(b, Hitbox):
            raise ValueError(f"{b} does not extend Hitbox")

        if b not in hitbox_types:
            raise ValueError(
                f"{type(b)} not registered with collisions.py. "
                f"try calling new_hitbox_type({type(b)})"
            )
        else:
            b = hitbox_types.index(b)

    if not callable(func):
        raise ValueError(f"{func}: passed non-callable to set_collider")

    # Actual function

    colliders[(a, b)] = func
    colliders[(b, a)] = lambda x, y: func(y, x)


class Hitbox(ABC):
    pass


class CollisionEvent:
    pass


class CollisionLayer:
    pass
