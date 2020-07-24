import pygame
import os
import sys
import numpy as np

from inputs import Paddle, Counter, KeyDispatcher
from classes import FloatRect
from camera import Scene, SpriteCircle, SpriteGrid, SpriteRectangle, Camera

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

pg = pygame


# Rendering parameters

WINDOWSIZE = np.array([900, 600])
SCALE = 100.0


# Game parameters

TICKRATE = 100
DT = 1 / TICKRATE


class GameState:

    def __init__(self, triggers, scene, camera):
        pass

    def update(self):
        pass


def init_camera(screen):

    scene = Scene()
    camera = Camera(screen, scene, scale=SCALE)

    return scene, camera


def init_inputs():

    keydispatcher = KeyDispatcher()
    triggers = []

    return keydispatcher, triggers


def main():

    # Prepare rendering
    screen = pygame.display.set_mode(WINDOWSIZE)
    scene, camera = init_camera(screen)

    # Prepare inputs
    keydispatcher, ks_triggers = init_inputs()

    # Prepare game state
    gamestate = GameState(ks_triggers, scene, camera)

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

        gamestate.update()

        camera.draw()
        pygame.display.flip()

        clock.tick(TICKRATE)


if __name__ == "__main__":
    main()
