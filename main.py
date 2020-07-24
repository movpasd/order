import pygame
import os
import sys
import numpy as np

from camera import Scene, SpriteCircle, SpriteRectangle, Camera

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"


# Rendering parameters

RED = (255, 0, 0)

WINDOWSIZE = np.array([900, 600])
ORIGIN = WINDOWSIZE / 2
SCALE = 25.0


# Game parameters

TICKRATE = 100
DT = 1 / TICKRATE


def main():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOWSIZE)

    sprect = SpriteRectangle(0.5, 0.5, 1, 1, thickness=1)
    scene = Scene(sprites=[sprect])
    camera = Camera(screen, scene)

    running = True
    while running:

    	for event in pygame.event.get():
    		if event.type == pygame.QUIT: sys.exit()

    	camera.draw()
    	pygame.display.flip()

    	clock.tick(TICKRATE)


if __name__ == "__main__":
    main()
