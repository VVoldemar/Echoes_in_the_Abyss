"""Файл для хранения классов спрайтов: Tile (тайл/клетка поля) и Player (игрок)"""

import pygame
from config import COIN_IMG, EMPTY_IMG, FINISH_IMG, PLAYER_IMG, SPIKES_IMG, TILE_SIZE, TRAMPOLINE_IMG, WALL_IMG  # Импортируем константу размера тайла
from utils import load_image # Импортируем функцию загрузки изображений
directions = {
    'left': 180,
    'right': 0,
    'down': 270,
    'up': 90,
    'l': 180,
    'r': 0,
    'd': 270,
    'u': 90,
    'g': 180,
    'j': 0,
    'y': 270,
    'h': 90
}
# Загрузка изображений тайлов и игрока (эти изображения используются в классах Tile и Player)
tile_images = {
    'wall': load_image(WALL_IMG), # Изображение стены
    'empty': load_image(EMPTY_IMG), # Изображение пустой клетки
    'trampoline': load_image(TRAMPOLINE_IMG), # Изображение трамплина
    'finish': load_image(FINISH_IMG), # Изображение трамплина
    'spikes': load_image(SPIKES_IMG), # Изображение трамплина
    'coin': load_image(COIN_IMG), # Изображение трамплина
}
player_image = load_image(PLAYER_IMG) # Изображение игрока


# Класс Tile (тайл/клетка поля)
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, groups, direction=None):
        """
        Конструктор класса Tile.

        Args:
            tile_type (str): Тип тайла ('wall' или 'empty').
            pos_x (int): Позиция тайла по оси X (в тайлах).
            pos_y (int): Позиция тайла по оси Y (в тайлах).
            groups (list): Список групп спрайтов, к которым нужно добавить тайл.
        """
        super().__init__(groups)  # Добавляем спрайт в указанные группы
        self.tile_type = tile_type
        self.image = tile_images[tile_type]  # Устанавливаем изображение тайла в зависимости от его типа
        if direction is not None:
            self.image = pygame.transform.rotate(self.image, directions[direction])

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
        self.tile_type = 'player'
        self.moving = False # Флаг, указывающий, находится ли игрок в движении
        self.image = player_image  # Устанавливаем изображение игрока
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)  # Получаем прямоугольник изображения и устанавливаем его в начальную позицию
        self.speed = 16
        self.nextmove = None
    def move(self, level, direction=None):
        """
        Перемещает игрока в указанном направлении.

        Args:
            level (list): Двумерный список, представляющий карту уровня.
            direction (str, optional): Направление движения ('up', 'down', 'left', 'right'). Defaults to None.
                                        Если direction не указан, продолжает движение в текущем направлении.
        """

        if direction is not None and not self.moving:  # Если задано новое направление, меняем текущее направление
            self.direction = direction
        if self.moving and direction is not None:
            self.nextmove = direction
        self.moving = True  # Устанавливаем флаг движения в True
        if self.direction == 'left':
            if level[self.rect.y // TILE_SIZE][(self.rect.x - 1) // TILE_SIZE] == '#':  # Проверка на столкновение со стеной слева
                self.moving = False  # Если стена, останавливаем движение
                return
            self.rect.x -= self.speed  # Сдвигаем позицию игрока влево на self.speed пикселей
        elif self.direction == 'right':
            if level[self.rect.y // TILE_SIZE][(self.rect.x) // TILE_SIZE + 1] == '#':  # Проверка на столкновение со стеной справа
                self.moving = False  # Если стена, останавливаем движение
                return
            self.rect.x += self.speed  # Сдвигаем позицию игрока вправо на self.speed пикселей
        elif self.direction == 'up':
            if level[(self.rect.y - 1) // TILE_SIZE][self.rect.x // TILE_SIZE] == '#':  # Проверка на столкновение со стеной сверху
                self.moving = False  # Если стена, останавливаем движение
                return
            self.rect.y -= self.speed  # Сдвигаем позицию игрока вверх на self.speed пикселей
        elif self.direction == 'down':
            if level[self.rect.y // TILE_SIZE + 1][self.rect.x // TILE_SIZE] == '#':  # Проверка на столкновение со стеной снизу
                self.moving = False  # Если стена, останавливаем движение
                return
            self.rect.y += self.speed  # Сдвигаем позицию игрока вниз на self.speed пикселей
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, directions[self.direction])
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)  # Обновляем позицию прямоугольника спрайта