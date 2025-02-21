"""Файл для хранения вспомогательных функций, таких как загрузка изображений и уровней"""

import pygame
import sys
import os


def terminate():
    """
    Закрывает окно.
    """
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """
    Загружает изображение из папки 'img'.

    Args:
        name (str): Имя файла изображения.
        colorkey (optional): Цвет, который нужно сделать прозрачным. Defaults to None.

    Returns:
        pygame.Surface: Загруженное изображение.
    """
    fullname = os.path.join(
        'img', name)  # Формируем полный путь к файлу изображения
    if not os.path.isfile(fullname):  # Проверяем, существует ли файл
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def get_font(size):
    return pygame.font.Font("fonts/font.ttf", size)


def load_level(filename):
    """
    Загружает уровень из текстового файла.

    Args:
        filename (str): Имя файла уровня.

    Returns:
        list: Двумерный список, представляющий карту уровня.
    """
    filename = "levels/" + filename  # Формируем путь к файлу уровня
    with open(filename, 'r') as mapFile:
        # Читаем строки из файла, удаляя пробельные символы в начале и конце
        level_map = [line.strip() for line in mapFile]

    # Находим максимальную ширину строки в уровне
    max_width = max(map(len, level_map))

    # Выравниваем все строки уровня до максимальной ширины, заполняя 'e' в конце более коротких строк
    return list(map(lambda x: list(x.ljust(max_width, 'e')), level_map))


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)

        self.camera = pygame.Rect(x, y, self.width, self.height)

    def move(self, dx, dy):
        x = -dx
        y = -dy

        self.camera = pygame.Rect(x, y, self.width, self.height)


tile_to_symbol = {
    'player': 'p',
    'wall': '#',
    'empty': 'e',
    'finish': 'f',
    'coin': 'c',
    'spikesy': 'y',
    'spikesg': 'g',
    'spikesh': 'h',
    'spikesj': 'j',
    'trampolinel': 'l',
    'trampoliner': 'r',
    'emptyd': 'e'
}
