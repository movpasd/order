import pygame as pg
import numpy as np
from pathlib import Path
import os

import render
from render.scenes import Scene, Camera, Sprite, SpriteCircle
import inputs.keyboard
import inputs.controllers
import utils.floatshapes as fs
import entity, entity.mobs


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


PATH_ASSETS = Path(__file__).parents[0] / "assets"


SPEED = 5.
ANGSPEED = 90


class GameState:

    def __init__(self, keydispatcher, rendermanager):

        # Prepare inputs
        self.paddle = inputs.controllers.Paddle()
        self.paddle.bind(keydispatcher, BINDS_PADDLE)

        # Prepare scene
        self.camera = Camera(WINDOWSIZE, scale=SCALE)
        self.scene = Scene(self.camera, bg=(128, 128, 128))
        rendermanager.renderables.append(self.scene)

        # Prepare mobs
        surf = pg.image.load(str(PATH_ASSETS / "smiley.png"))

        self.mob1 = entity.mobs.MyMob(surf, 0, 0, 0)
        self.mob1.add_to_scene(self.scene)

        self.mob2 = entity.mobs.MyMob2(surf, 1, 0, 0)
        self.mob2.add_to_scene(self.scene)


    def tick(self, dt):

        self.mob1.pos += SPEED * self.paddle.vector * dt
        self.mob1.tick(dt)
        self.mob2.tick(dt)


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
