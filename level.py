"""Файл для функций, связанных с генерацией и управлением уровнями"""

from sprites import Tile, Player # Импортируем классы Tile и Player
from utils import load_level # Импортируем функцию загрузки уровня

def generate_level(level_filename, all_sprites, tiles_group, player_group):
    """
    Генерирует уровень из файла.

    Args:
        level_filename (str): Имя файла уровня.
        all_sprites (pygame.sprite.Group): Группа для всех спрайтов.
        tiles_group (pygame.sprite.Group): Группа для спрайтов тайлов.
        player_group (pygame.sprite.Group): Группа для спрайтов игрока.

    Returns:
        tuple: Кортеж, содержащий объект игрока и двумерный список, представляющий карту уровня.
    """
    level = load_level(level_filename) # Загружаем карту уровня из файла
    new_player, x, y = None, None, None # Инициализируем переменные для игрока и координат
    for y in range(len(level)): # Перебираем строки карты уровня
        for x in range(len(level[y])): # Перебираем символы в строке
            if level[y][x] == '0': # Если символ '.' - пустая клетка
                Tile('empty', x, y, [tiles_group, all_sprites]) # Создаем тайл пустой клетки
            elif level[y][x] == '#': # Если символ '#' - стена
                Tile('wall', x, y, [tiles_group, all_sprites]) # Создаем тайл стены
            elif level[y][x] == 'l' or level[y][x] == 'r': # Если символ 'r' или 'l' - трамплин
                Tile('trampoline', x, y, [tiles_group, all_sprites], direction=level[y][x]) # Создаем тайл трамплина
            elif level[y][x] == 'f': # Если символ 'f' - финишь
                Tile('finish', x, y, [tiles_group, all_sprites]) # Создаем тайл трамплина
            elif level[y][x] == '@': # Если символ '@' - начальная позиция игрока
                Tile('empty', x, y, [tiles_group, all_sprites]) # Создаем тайл пустой клетки под игроком
                new_player = Player(x, y, [player_group, all_sprites]) # Создаем игрока в указанной позиции
    return new_player, level # Возвращаем объект игрока и карту уровня