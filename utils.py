"""Файл для хранения вспомогательных функций, таких как загрузка изображений и уровней"""

import pygame
import sys
import os


def load_image(name, colorkey=None):
    """
    Загружает изображение из папки 'img'.

    Args:
        name (str): Имя файла изображения.
        colorkey (optional): Цвет, который нужно сделать прозрачным. Defaults to None.

    Returns:
        pygame.Surface: Загруженное изображение.
    """
    fullname = os.path.join('img', name) # Формируем полный путь к файлу изображения
    if not os.path.isfile(fullname): # Проверяем, существует ли файл
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
        level_map = [line.strip() for line in mapFile]  # Читаем строки из файла, удаляя пробельные символы в начале и конце

    max_width = max(map(len, level_map))  # Находим максимальную ширину строки в уровне

    # Выравниваем все строки уровня до максимальной ширины, заполняя '.' в конце более коротких строк
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))