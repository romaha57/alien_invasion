import pygame
from pygame.sprite import Group

import settings
from spaceship import SpaceShip
from events_handler import _check_events
from aliens import create_army
from stats import Stats
from scores import Score


def run_game() -> None:
    """Функция инициализации экрана(размеры экрана) и корабля"""

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                                     pygame.RESIZABLE)
    pygame.display.set_caption(settings.TITLE_GAME)
    pygame.display.set_icon(pygame.image.load('images/icon.png'))
    pygame.mouse.set_visible(False)  # скрываем курсор на экране игры

    spaceship = SpaceShip(screen=screen)
    aliens = Group()
    create_army(screen=screen, aliens=aliens)
    bullets = Group()

    stats = Stats()    # загружаем статистику игры
    score = Score(screen=screen, stats=stats)

    while True:   # цикл игры

        clock.tick(settings.FPS)  # ограничивает частоту прохода цикла

        _check_events(screen, spaceship, bullets)
        if stats.run_game:
            screen.fill(settings.BG_COLOR)

            for bullet in bullets.sprites():
                bullet.draw_bullet()
                bullet.move_bullet()

            aliens.draw(screen)
            aliens.update(stats, screen, spaceship, aliens, bullets, score)
            bullets.update(screen, bullets, aliens, stats, score)

            score.draw_score()  # выводим счет и рекорд на экран

            spaceship.draw_spaceship()
            spaceship.move_spaceship()

            pygame.display.flip()  # отображаем последний экран игры


if __name__ == '__main__':
    run_game()
