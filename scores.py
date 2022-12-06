from pygame.font import SysFont
from pygame.sprite import Group

import settings
from spaceship import SpaceShip


class Score:
    """Класс для отображения очков игры"""

    def __init__(self, screen, stats):
        """Инициализация очков игры и вызов функций для отображения на экране"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.text_color = settings.TEXT_COLOR

        # подгружаем шрифты(берем стандартный - None)
        self.font = SysFont(None, 35)

        # функции отображения очков игры, рекорда, жизней
        self.image_score()
        self.image_high_score()
        self.image_health()

    def image_score(self):
        """Преобразовывает текст счета в графическое изображение"""

        self.score_img = self.font.render(str(self.stats.score),
                                          True, self.text_color, (settings.BG_COLOR))
        self.score_rect = self.score_img.get_rect()

        # размещение счета на экране по координатам
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20

    def image_high_score(self):
        """Преобразовыввает рекорд счета в графическое изображение"""

        self.high_score_img = self.font.render(str(self.stats.high_score),
                                               True, self.text_color, (settings.BG_COLOR))
        self.high_score_rect = self.high_score_img.get_rect()

        # размещение рекорда на экране по координатам
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def image_health(self):
        """Отображает количество жизней корабля"""

        self.spaceships = Group()
        for spaceship_health in range(self.stats.health):
            spaceship = SpaceShip(self.screen)

            # отображаем жизни корабля слева сверху
            spaceship.rect.x = 15 + spaceship_health * spaceship.rect.width
            spaceship.rect.y = 20
            self.spaceships.add(spaceship)

    def draw_score(self):
        """Функция для отрисовки очков игры, рекорда и жизней на экране"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.spaceships.draw(self.screen)


def check_high_score(stats, score):
    """Проверка на новый рекорд"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score

        # перезаписываем рекорд в файл
        with open('highscore.txt', 'w') as file:
            file.write(str(stats.high_score))
