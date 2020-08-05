import pygame as pg
import numpy as np
from pathlib import Path
import os

import render
from render.scenes import Scene, Camera, Sprite, SpriteCircle, SpriteRect
import inputs.keyboard
import inputs.controllers
from utils.floatshapes import FloatRect, FloatCircle
from utils.collide import collidevector


os.environ['SDL_VIDEO_CENTERED'] = '1'


WINDOWSIZE = (900, 600)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TPS = 100
DT = 1 / TPS

SCALE = 64.0

BINDS_PADDLE = {
    "north": pg.K_w,
    "west": pg.K_a,
    "east": pg.K_d,
    "south": pg.K_s,
}

BINDS_CAMERAPAD = {
    "north": pg.K_UP,
    "west": pg.K_LEFT,
    "east": pg.K_RIGHT,
    "south": pg.K_DOWN,
}

BINDS_CAMZOOM = {
    "decrement": pg.K_o,
    "increment": pg.K_p,
}


PATH_ASSETS = Path(__file__).parents[0] / "assets"


CAMSPEED = 10.
PSPEED = 5.


class GameState:

    def __init__(self, keydispatcher, rendermanager):

        # Prepare inputs

        self.paddle = inputs.controllers.Paddle()
        self.paddle.bind(keydispatcher, BINDS_PADDLE)

        self.campad = inputs.controllers.Paddle()
        self.campad.bind(keydispatcher, BINDS_CAMERAPAD)

        self.camzoom = inputs.controllers.Counter()
        self.camzoom.bind(keydispatcher, BINDS_CAMZOOM)

        # Prepare scene

        self.camera = Camera(WINDOWSIZE)
        self.scene = Scene(self.camera, bg=WHITE)
        rendermanager.renderables.append(self.scene)

        # Prepare game objects

        self.wallrect = FloatRect(2, -2, 3, 6)
        self.circle = FloatCircle(-2, 0, 1)
        self.playercircle = FloatCircle(0, 0, 1)

        # self.playersprite = SpriteCircle.from_circle(BLUE, self.playercircle)
        self.wallsprite = SpriteRect(BLACK, self.wallrect)
        self.circlesprite = SpriteCircle.from_circle(BLUE, self.circle)
        sf = pg.image.load(str(PATH_ASSETS / "smiley.png"))
        sf.convert()
        self.playersprite = Sprite(sf, self.playercircle.get_rect())

        self.scene.add_sprite(self.playersprite)
        self.scene.add_sprite(self.wallsprite)
        self.scene.add_sprite(self.circlesprite)

    def tick_cam(self, dt):

        self.camera.center += CAMSPEED * dt * self.campad.vector
        self.camera.scale = SCALE * 2 ** self.camzoom.count

    def tick_player(self, dt):

        vec = self.paddle.vector * PSPEED * dt
        self.playercircle = self.playercircle.shifted(*vec)

        cv1 = collidevector(self.playercircle, self.circle)
        self.circle = self.circle.shifted(*- cv1 / 2)

        cv2 = collidevector(self.playercircle, self.wallrect)
        self.playercircle = self.playercircle.shifted(*(cv1 / 2 + cv2))

        self.playersprite.rect = self.playercircle.get_rect()
        self.circlesprite.rect = self.circle.get_rect()

    def tick(self, dt):

        self.tick_cam(dt)
        self.tick_player(dt)


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
