import pygame
from pygame.sprite import Sprite

import settings


class SpaceShip(Sprite):
    """Класс для создания космического корабля, его отрисовки на экране и передвижении"""

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__()
        self.screen = screen
        self.raw_image = pygame.image.load('images/spaceship.png')
        self.image = pygame.transform.scale(self.raw_image,
                                            (settings.SPACESHIP_SIZE_HEIGHT,
                                             settings.SPACESHIP_SIZE_WIDTH))

        self.rect = self.image.get_rect()   # получаем объект rect для корабля

        self.screen_rect = screen.get_rect() # получаем объект rect для экрана

        self.rect.centerx = self.screen_rect.centerx  # размещаем корабль на экране по координатам
        self.rect.bottom = self.screen_rect.bottom

        # добавляем для возможности установить значения перемещения типа float
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        self.move_right = False
        self.move_left = False        # флаги для переключения клавиши "нажата/не нажата"
        self.move_up = False
        self.move_down = False

    def draw_spaceship(self) -> None:
        """Отрисовываем корабль на экране"""

        self.screen.blit(self.image, self.rect)

    def move_spaceship(self) -> None:
        """Функция по перемещение корабля на экране"""

        if self.move_right and self.rect.right <= self.screen_rect.right:  # перемещение вправо
            self.center_x += settings.SPACESHIP_SPEED

        if self.move_left and self.rect.left >= 0:                         # перемещение влево
            self.center_x -= settings.SPACESHIP_SPEED

        if self.move_up and self.rect.top >= 0:                            # перемещение вверх
            self.center_y -= settings.SPACESHIP_SPEED

        if self.move_down and self.rect.bottom <= self.screen_rect.bottom:  # перемещение вниз
            self.center_y += settings.SPACESHIP_SPEED

        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def create_spaceship(self) -> None:
        """Функция создания корабля в центре экрана(после гибели)"""

        self.center_x = self.screen_rect.bottom
        self.center_y = self.screen_rect.bottom
