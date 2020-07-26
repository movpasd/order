import pygame
import os
import sys
import numpy as np

import collisions
from inputs.keyboard import KeyDispatcher
from inputs.controllers import Paddle, Counter
from utils import FloatRect
from scenes.camera import Camera
from scenes.sprites import Scene, SpriteCircle, SpriteGrid, SpriteRectangle

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

pg = pygame


# Rendering parameters

WINDOWSIZE = np.array([900, 600])
SCALE = 100.0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Game parameters

TICKRATE = 100
DT = 1 / TICKRATE

CAM_SPEED = 5.0
ZOOM_DELTA = 10.0
ZOOM_COUNTER_INIT = 0
ZOOM_COUNTER_MIN = -5
ZOOM_COUNTER_MAX = 5
ZOOM_MULTIPLIER = 1.5
INIT_SCALE = ZOOM_MULTIPLIER ** ZOOM_COUNTER_INIT * SCALE

BALL_SPEED = 5.0


class GameState:

    def __init__(self, scene, camera, paddle, arrows, zoom):

        self.scene = scene
        self.camera = camera
        self.paddle = paddle
        self.arrows = arrows
        self.zoom = zoom

        self.create_scene()

    def create_scene(self):

        scene = self.scene
        scene.add_sprite(SpriteCircle(0, 0, 0.1, color=RED, thickness=0))
        scene.add_sprite(SpriteGrid(0, 0, 1))

        # Controllable ball
        scene.add_sprite(SpriteCircle(0, 0, 0.1, color=RED))

    def update(self, dt):

        self.camera.scale = ZOOM_MULTIPLIER ** self.zoom.count * SCALE
        self.camera.center += CAM_SPEED * self.paddle.vector * dt
        self.scene.sprites[-1].pos += BALL_SPEED * self.arrows.vector * dt


def init_camera(screen):

    scene = Scene()
    camera = Camera(screen, scene, scale=INIT_SCALE)

    return scene, camera


def init_inputs():

    keydispatcher = KeyDispatcher()

    return keydispatcher


def main():

    # Prepare rendering
    screen = pygame.display.set_mode(WINDOWSIZE)
    scene, camera = init_camera(screen)

    # Prepare inputs
    keydispatcher = init_inputs()

    paddle_bindings = {
        "north": pg.K_w,
        "south": pg.K_s,
        "east": pg.K_d,
        "west": pg.K_a
    }

    paddle = Paddle()
    paddle.bind(keydispatcher, paddle_bindings)

    arrows_bindings = {
        "north": pg.K_UP,
        "south": pg.K_DOWN,
        "east": pg.K_RIGHT,
        "west": pg.K_LEFT
    }

    arrows = Paddle()
    arrows.bind(keydispatcher, arrows_bindings)

    zoom_bindings = {
        "increment": pg.K_RIGHTBRACKET,
        "decrement": pg.K_LEFTBRACKET
    }

    zoom = Counter(vinit=ZOOM_COUNTER_INIT,
                   vmin=ZOOM_COUNTER_MIN, vmax=ZOOM_COUNTER_MAX)
    zoom.bind(keydispatcher, zoom_bindings)

    # Prepare game state
    gamestate = GameState(scene, camera, paddle, arrows, zoom)

    # Prepare clock
    clock = pygame.time.Clock()

    # MAIN LOOP
    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                keydispatcher.dispatch(event)

        gamestate.update(DT)

        camera.draw()
        pygame.display.flip()

        clock.tick(TICKRATE)


if __name__ == "__main__":
    main()
