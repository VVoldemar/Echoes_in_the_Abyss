"""Файл для хранения классов спрайтов: Tile (тайл/клетка поля) и Player (игрок)"""

import pygame
from config import TILE_SIZE  # Импортируем константу размера тайла
from utils import load_image # Импортируем функцию загрузки изображений

# Загрузка изображений тайлов и игрока (эти изображения используются в классах Tile и Player)
tile_images = {
    'wall': load_image('wall.png'), # Изображение стены
    'empty': load_image('empty.png'), # Изображение пустой клетки
}
player_image = load_image('player.png') # Изображение игрока


# Класс Tile (тайл/клетка поля)
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, groups):
        """
        Конструктор класса Tile.

        Args:
            tile_type (str): Тип тайла ('wall' или 'empty').
            pos_x (int): Позиция тайла по оси X (в тайлах).
            pos_y (int): Позиция тайла по оси Y (в тайлах).
            groups (list): Список групп спрайтов, к которым нужно добавить тайл.
        """
        super().__init__(groups)  # Добавляем спрайт в указанные группы
        self.image = tile_images[tile_type]  # Устанавливаем изображение тайла в зависимости от его типа
        self.rect = self.image.get_rect().move(  # Получаем прямоугольник изображения и смещаем его на нужную позицию
            TILE_SIZE * pos_x, TILE_SIZE * pos_y)


# Класс Player (игрок)
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, groups):
        """
        Конструктор класса Player.

        Args:
            pos_x (int): Начальная позиция игрока по оси X (в тайлах).
            pos_y (int): Начальная позиция игрока по оси Y (в тайлах).
            groups (list): Список групп спрайтов, к которым нужно добавить игрока.
        """
        super().__init__(groups)  # Добавляем спрайт в указанные группы
        self.direction = ''  # Начальное направление движения игрока
        self.pos = {  # Позиция игрока в пикселях
            'x': TILE_SIZE * pos_x,
            'y': TILE_SIZE * pos_y,
        }
        self.moving = False # Флаг, указывающий, находится ли игрок в движении
        self.image = player_image  # Устанавливаем изображение игрока
        self.rect = self.image.get_rect().move(self.pos['x'], self.pos['y'])  # Получаем прямоугольник изображения и устанавливаем его в начальную позицию

    def move(self, level, direction=None):
        """
        Перемещает игрока в указанном направлении.

        Args:
            level (list): Двумерный список, представляющий карту уровня.
            direction (str, optional): Направление движения ('up', 'down', 'left', 'right'). Defaults to None.
                                        Если direction не указан, продолжает движение в текущем направлении.
        """
        if direction is not None:  # Если задано новое направление, меняем текущее направление
            self.direction = direction
        self.moving = True  # Устанавливаем флаг движения в True
        # TODO make special constant for step
        if self.direction == 'left':
            if level[(self.pos['x'] - 1) // TILE_SIZE][self.pos['y'] // TILE_SIZE] == '#':  # Проверка на столкновение со стеной слева
                self.moving = False  # Если стена, останавливаем движение
                return
            self.pos['x'] -= 5  # Сдвигаем позицию игрока влево на 5 пикселей
        elif self.direction == 'right':
            if level[(self.pos['x']) // TILE_SIZE + 1][self.pos['y'] // TILE_SIZE] == '#':  # Проверка на столкновение со стеной справа
                self.moving = False  # Если стена, останавливаем движение
                return
            self.pos['x'] += 5  # Сдвигаем позицию игрока вправо на 5 пикселей
        elif self.direction == 'up':
            if level[self.pos['x'] // TILE_SIZE][(self.pos['y'] - 1) // TILE_SIZE] == '#':  # Проверка на столкновение со стеной сверху
                self.moving = False  # Если стена, останавливаем движение
                return
            self.pos['y'] -= 5  # Сдвигаем позицию игрока вверх на 5 пикселей
        elif self.direction == 'down':
            if level[self.pos['x'] // TILE_SIZE][self.pos['y'] // TILE_SIZE + 1] == '#':  # Проверка на столкновение со стеной снизу
                self.moving = False  # Если стена, останавливаем движение
                return
            self.pos['y'] += 5  # Сдвигаем позицию игрока вниз на 5 пикселей
        self.rect = self.image.get_rect().move(self.pos['x'], self.pos['y'])  # Обновляем позицию прямоугольника спрайта