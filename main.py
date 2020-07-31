import pygame as pg
import numpy as np
from pathlib import Path
import os

import render
from render.scenes import Scene, Camera, Sprite, SpriteCircle
import inputs.keyboard
import inputs.controllers
import utils.floatshapes as fs


os.environ['SDL_VIDEO_CENTERED'] = '1'


WINDOWSIZE = (900, 600)
BGC = (255, 255, 255)

TPS = 100
DT = 1 / TPS

SCALE = 128.0

BINDS_PADDLE = {
    "north": pg.K_w,
    "west": pg.K_a,
    "east": pg.K_d,
    "south": pg.K_s,
}

BINDS_ZOOM = {
    "increment": pg.K_p,
    "decrement": pg.K_o,
}

BINDS_ROTATE = {
    "increase": pg.K_PERIOD,
    "decrease": pg.K_COMMA,
}


PATH_ASSETS = Path(__file__).parents[0] / "assets"


SPEED = 5.
ANGSPEED = 90


class GameState:

    def __init__(self, keydispatcher, rendermanager):

        self.paddle = inputs.controllers.Paddle()
        self.paddle.bind(keydispatcher, BINDS_PADDLE)

        self.zoomcounter = inputs.controllers.Counter()
        self.zoomcounter.bind(keydispatcher, BINDS_ZOOM)

        self.angleslider = inputs.controllers.Slider()
        self.angleslider.bind(keydispatcher, BINDS_ROTATE)

        self.camera = Camera(WINDOWSIZE, scale=SCALE)
        self.scene = Scene(self.camera, bg=BGC)
        rendermanager.renderables.append(self.scene)

        smile = pg.image.load(str(PATH_ASSETS / "smiley.png"))
        rect = fs.FloatRect.from_center(0.5, 0.5, 1, 1)
        spr = Sprite(smile, rect)

        shrect = rect
        shrect = shrect.shifted(0, -0.5)
        shrect = shrect.xyscaled(0.9, 0.2)

        sh = SpriteCircle((0, 0, 0), shrect, alpha=64, z=-0.1)

        self.scene.sprites.append(spr)
        self.scene.sprites.append(sh)

        self.smile = spr
        self.sh = sh

    def tick(self, dt):

        self.smile.pos += self.paddle.vector * SPEED * dt
        self.sh.pos = self.smile.pos + np.array((0, -0.5))
        self.smile.angle += self.angleslider.value * ANGSPEED * dt

        self.camera.scale = SCALE * 2 ** self.zoomcounter.count


def main():

    pg.init()
    screen = pg.display.set_mode(size=WINDOWSIZE)

    keydispatcher = inputs.keyboard.KeyDispatcher()
    rendermanager = render.RenderManager(screen)

    gamestate = GameState(keydispatcher, rendermanager)

    clock = pg.time.Clock()

    running = True
    while running:

        for e in pg.event.get():

            if e.type == pg.QUIT:
                running = False

            if e.type == pg.KEYUP or e.type == pg.KEYDOWN:
                keydispatcher.dispatch(e)

        gamestate.tick(DT)

        rendermanager.update()
        pg.display.flip()

        clock.tick(TPS)


if __name__ == "__main__":
    main()
