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

RED = (255, 0, 0)
BLUE = (0, 0, 255)

WINDOWSIZE = np.array([900, 600])
ORIGIN = WINDOWSIZE / 2
SCALE = 100.0


# Game parameters

TICKRATE = 100
DT = 1 / TICKRATE


def main():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOWSIZE)

    br = FloatRect(-5, 5, 10, 10)
    sprect = SpriteRectangle(-1, 4, 2.2, 0.4, color=RED)
    origincircle = SpriteCircle(0, 0, 0.2, color=RED, thickness=1)
    spgrid = SpriteGrid(0, 0, 1, boundrect=br)
    sprect2 = SpriteRectangle.from_floatrect(br, color=BLUE, thickness=1)

    scene = Scene(sprites=[sprect, spgrid, origincircle, sprect2])
    camera = Camera(screen, scene, scale=SCALE)

    keydispatcher = KeyDispatcher()
    paddle = Paddle()
    counter = Counter(4, 1, 10)

    paddle.bind(keydispatcher, pg.K_a, pg.K_d, pg.K_w, pg.K_s)
    counter.bind(keydispatcher, pg.K_1, pg.K_2)

    v = 1000.0

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                keydispatcher.dispatch(event)

        camera.center += paddle.vector * v / SCALE * DT
        camera.scale = SCALE / counter.count

        camera.draw()
        pygame.display.flip()

        clock.tick(TICKRATE)


if __name__ == "__main__":
    main()
