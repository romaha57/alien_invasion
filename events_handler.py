import sys

import pygame
from pygame.sprite import Group
from pygame.mixer import Sound

from bullets import Bullet
from spaceship import SpaceShip
import settings


def _check_events(screen: pygame.Surface, spaceship: SpaceShip,
                  bullets: Group, sound_shot: Sound) -> None:
    """Функция для обработки событий (клавиши left, right, up, down, space)"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # обрабатываем нажатие клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                spaceship.move_right = True
            elif event.key == pygame.K_LEFT:
                spaceship.move_left = True
            elif event.key == pygame.K_UP:
                spaceship.move_up = True
            elif event.key == pygame.K_DOWN:
                spaceship.move_down = True
            elif event.key == pygame.K_SPACE:
                sound_shot.play()
                new_bullet = Bullet(screen=screen, spaceship=spaceship)
                bullets.add(new_bullet)
            elif event.key == pygame.K_RETURN:
                settings.RUN_GAME = True

        # обрабатываем отжатие клавиш
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                spaceship.move_right = False
            elif event.key == pygame.K_LEFT:
                spaceship.move_left = False
            elif event.key == pygame.K_UP:
                spaceship.move_up = False
            elif event.key == pygame.K_DOWN:
                spaceship.move_down = False
