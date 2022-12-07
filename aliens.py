import sys
import time

import pygame.image
from pygame.sprite import Sprite, Group

import settings
from stats import Stats
from scores import Score
from spaceship import SpaceShip


class Alien(Sprite):
    """Класс для пришельца"""

    def __init__(self, screen: pygame.Surface) -> None:
        """Создаем пришельца, подгружаем картинку
         и задаем ему координаты для отображения на экране"""

        super().__init__()

        self.screen = screen
        self.raw_image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale(self.raw_image,
                                            (settings.ALIEN_HEIGHT, settings.ALIEN_WIDTH))

        self.rect = self.image.get_rect()

        # задаем координаты для пришельца
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # преобразовываем для того, чтобы можно было указать float значения для плавности
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw_alien(self) -> None:
        """Отрисовываем пришельца на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self, stats: Stats, screen: pygame.Surface,
               spaceship: SpaceShip, aliens: Group, bullets: Group, score: Score) -> None:
        """Перемещение пришельца"""

        self.y += settings.ALIEN_SPEED
        self.rect.y = self.y

        # проверяем на коллизии пришельца и корабля
        if pygame.sprite.spritecollideany(spaceship, aliens):
            spaceship_death(stats, screen, spaceship, aliens, bullets, score)

        # коллизия пришельца и нижней границы экрана
        check_alien_go_border(stats, screen, spaceship, aliens, bullets, score)


def create_army(screen: pygame.Surface, aliens: Group) -> None:
    """Функция для рассчета и создания армии пришельцев"""

    alien = Alien(screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    # считаем сколько поместиться пришельцев на экране в ряду и столбце
    alien_count_x = int((settings.SCREEN_WIDTH - (2 * alien_width)) / alien_width)
    alien_count_y = int((settings.SCREEN_HEIGHT - settings.SPACESHIP_SIZE_HEIGHT -
                         (2 * alien_height)) / alien_height)

    # создаем пришельцев и задаем им координаты для отображения
    for al_row in range(alien_count_y - 5):
        for al_col in range(alien_count_x):
            alien = Alien(screen)
            alien.x = alien_width + alien_width * al_col
            alien.y = alien_height + alien_height * al_row
            alien.rect.x = alien.x
            alien.rect.y = alien.y

            aliens.add(alien)


def spaceship_death(stats: Stats, screen: pygame.Surface, spaceship: SpaceShip,
                    aliens: Group, bullets: Group, score: Score) -> None:
    """Функция для потери корабля"""

    if stats.health > 0:
        stats.health -= 1
        score.image_health()

        # удаляем все пули и пришельцев
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens)
        spaceship.create_spaceship()
        time.sleep(1)
    else:
        # при health=0 игра закрывается
        stats.run_game = False
        sys.exit()


def check_alien_go_border(stats: Stats, screen: pygame.Surface, spaceship: SpaceShip,
                          aliens: Group, bullets: Group, score: Score) -> None:
    """Функция для проверки пересечения нижней границы экрана и пришельца,
    если пересекается, то отнимается 1 жизнь"""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            spaceship_death(stats, screen, spaceship, aliens, bullets, score)
            break

