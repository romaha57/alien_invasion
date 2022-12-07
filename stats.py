class Stats:
    """Класс для статистики игры """

    def __init__(self) -> None:
        """Создание начальных параметров игры и чтения рекорда из файла"""

        self.health = 2
        self.run_game = True
        self.score = 0
        with open('highscore.txt', 'r') as file:
            self.high_score = int(file.readline())
