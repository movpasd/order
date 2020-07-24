import collisions


# HITBOX TYPES


class HitCircle(collisions.Hitbox):
    
    def __init__(self, center, radius):

        self.center = np.array(center, float)
        self.radius = float(radius)


class HitRect(collisions.Hitbox):
    pass


# COLLIDER FUNCTIONS


def _collider_cc(c1, c2):
    pass


def _collider_rr(r1, r2):
    pass


def _collider_rc(r, c):
    pass