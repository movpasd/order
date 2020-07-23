import pygame
import os
import sys
import numpy as np

from camera import Scene, Circle, Camera

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"


# Rendering parameters

RED = (255, 0, 0)

WINDOWSIZE = np.array([1500, 1000])
ORIGIN = WINDOWSIZE / 2
SCALE = 25.0


# Game parameters

TICKRATE = 1
DT = 1 / TICKRATE


def main():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOWSIZE)

    circle1 = Circle(0, 0, 4)
    scene = Scene(sprites=[circle1])
    camera = Camera(screen, scene)

    running = True
    while running:

    	for event in pygame.event.get():
    		if event.type == pygame.QUIT: sys.exit()

    	camera.draw()
    	pygame.display.flip()

    	circle1.pos += np.array([0, 5])

    	clock.tick(TICKRATE)


if __name__ == "__main__":
    main()
