import pygame
from pygame.sprite import Group

import settings
from spaceship import SpaceShip
from events_handler import _check_events
from aliens import create_army
from stats import Stats
from scores import Score


def run_game():
    """Функция инициализации экрана(размеры экрана) и корабля"""

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE_GAME)
    pygame.display.set_icon(pygame.image.load('images/icon.png'))

    spaceship = SpaceShip(screen=screen)
    aliens = Group()
    create_army(screen=screen, aliens=aliens)
    bullets = Group()

    # загружаем статистику игры
    stats = Stats()
    score = Score(screen=screen, stats=stats)

    # цикл игры
    while True:

        # цикл игры
        _check_events(screen, spaceship, bullets)
        if stats.run_game:
            screen.fill(settings.BG_COLOR)

            for bullet in bullets.sprites():
                bullet.draw_bullet()
                bullet.move_bullet()

            aliens.draw(screen)
            aliens.update(stats, screen, spaceship, aliens, bullets, score)
            bullets.update(screen, bullets, aliens, stats, score)

            # выводим счет и рекорд на экран
            score.draw_score()

            spaceship.draw_spaceship()
            spaceship.move_spaceship()

            # отображаем последний экран игры
            pygame.display.flip()


if __name__ == '__main__':
    run_game()
