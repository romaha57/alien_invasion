import time

import pygame
from pygame.sprite import Group
from pygame.font import SysFont

import settings
from spaceship import SpaceShip
from events_handler import _check_events
from aliens import create_army
from stats import Stats
from scores import Score


def run_game() -> None:
    """Функция инициализации экрана(размеры экрана) и корабля"""

    # пре-инит для звуков выстрела
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                                     pygame.RESIZABLE)
    pygame.display.set_caption(settings.TITLE_GAME)
    pygame.display.set_icon(pygame.image.load('images/icon.png'))
    pygame.mouse.set_visible(False)  # скрываем курсор на экране игры

    # подгружаем фон игры и подгоняем изображение по разрешение игры
    background = pygame.image.load('images/background.jpg').convert()
    background = pygame.transform.scale(background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    background_rect = background.get_rect()

    # подгружаем музыку для игры
    pygame.mixer.music.load('music/background_music.mp3')
    pygame.mixer.music.play(-1)
    sound_shot = pygame.mixer.Sound('music/sound_shot.wav')

    # выводим надписи перед игрой
    font = SysFont('arial', 50)
    text = font.render('Для начала игры нажмите enter', True, (211, 226, 73), (233, 75, 75))
    text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

    stats = Stats()  # загружаем статистику игры
    spaceship = SpaceShip(screen=screen)
    aliens = Group()
    create_army(screen=screen, aliens=aliens)
    bullets = Group()
    score = Score(screen=screen, stats=stats)

    while True:   # цикл игры

        clock.tick(settings.FPS)  # ограничивает частоту прохода цикла
        _check_events(screen, spaceship, bullets, sound_shot)
        if stats.run_game and settings.RUN_GAME:

            # отрисовываем фон игры
            screen.blit(background, background_rect)

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
