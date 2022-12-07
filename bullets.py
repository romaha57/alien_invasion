import pygame
from pygame.sprite import Sprite, Group

import settings
from aliens import create_army
from scores import check_high_score
from spaceship import SpaceShip
from stats import Stats
from scores import Score


class Bullet(Sprite):
    """Класс для инициализации пули и методы по отображению и перемещению ее"""

    def __init__(self, screen: pygame.Surface, spaceship: SpaceShip) -> None:
        """Иницилизация пули и назначение ей координат для отображения"""

        super().__init__()

        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.color = settings.BULLET_COLOR
        self.speed = settings.BULLET_SPEED

        # берем координаты для пули из положения корабля по координате Х
        # чтобы отрисовать пулю в верхней части и по центру корабля
        self.rect.centerx = spaceship.rect.centerx
        self.rect.top = spaceship.rect.top

        # преобразовываем для того, чтобы можно было указать float значения для плавности
        self.y = float(self.rect.y)

    def move_bullet(self) -> None:
        """Перемещение пули вверх"""

        self.y -= settings.BULLET_SPEED
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """Отрисовка пули на экране"""

        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self, screen: pygame.Surface, bullets: Group, aliens: Group,
               stats: Stats, score: Score) -> None:
        """Удаление пули, если она вылетела за экран"""

        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        # находим коллизии пули и пришельца
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if collisions:
            for collision in collisions.values():

                # увеличиваем количество очков за каждого пришельца на 10
                stats.score += 10 * len(collision)

            # проверяем текущие количество очков и рекорд и отображаем на экране
            check_high_score(stats)
            score.image_high_score()
            score.image_score()
            score.image_health()

        # если пришельцев на экране нет, то создаем новых
        if len(aliens) == 0:
            bullets.empty()
            create_army(screen, aliens)
