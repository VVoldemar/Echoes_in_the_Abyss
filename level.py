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
    total_coins = 0
    level_sprites = [[0] * 2*len(level[0]) for _ in range(len(level))]
    for y in range(len(level)): # Перебираем строки карты уровня
        for x in range(len(level[y])): # Перебираем символы в строке
            if level[y][x] == 'e': # Если символ '.' - пустая клетка
                level_sprites[y][x] = Tile('empty', x, y, [tiles_group, all_sprites]) # Создаем тайл пустой клетки
            elif level[y][x] == '#': # Если символ '#' - стена
                level_sprites[y][x] = Tile('wall', x, y, [tiles_group, all_sprites]) # Создаем тайл стены
            elif level[y][x] in 'lr': # Если символ 'r' или 'l' - трамплин
                level_sprites[y][x] = Tile('trampoline', x, y, [tiles_group, all_sprites], direction=level[y][x]) # Создаем тайл трамплина
            elif level[y][x] in 'yghj': # Если символ 's' - финишь
                level_sprites[y][x] = Tile('spikes', x, y, [tiles_group, all_sprites], direction=level[y][x]) # Создаем тайл шипов
            elif level[y][x] == 'f': # Если символ 'f' - финишь
                level_sprites[y][x] = Tile('finish', x, y, [tiles_group, all_sprites]) # Создаем тайл финиша
            elif level[y][x] == 'c': # Если символ 'f' - финишь
                level_sprites[y][x] = Tile('coin', x, y, [tiles_group, all_sprites]) # Создаем тайл монеты
                total_coins += 1
            elif level[y][x] == 'p': # Если символ '@' - начальная позиция игрока
                level_sprites[y][x] = Tile('empty', x, y, [tiles_group, all_sprites]) # Создаем тайл пустой клетки под игроком
                new_player = Player(x, y, [player_group, all_sprites]) # Создаем игрока в указанной позиции
    return new_player, level, level_sprites,  total_coins,  # Возвращаем объект игрока и карту уровня