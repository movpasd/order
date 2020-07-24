import collisions
import hitboxes as _hb

HitCircle = _hb.HitCircle
HitRect = _hb.HitRect


collisions.new_hitbox_type(HitCircle)

collisions.set_collider(HitCircle, HitCircle, _hb._collider_cc)


collisions.new_hitbox_type(HitRect)

collisions.set_collider(HitRect, HitCircle, _hb._collider_rc)
collisions.set_collider(HitRect, HitRect, _hb._collider_rr)