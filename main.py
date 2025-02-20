import pygame
from config import BG_IMG, TILE_SIZE, WIDTH, HEIGHT, FPS # Импортируем константы из config.py
from sprites import Tile
from utils import load_image, terminate # Импортируем функцию загрузки изображений
from level import generate_level # Импортируем функцию генерации уровня

# Инициализация Pygame
pygame.init()

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Echoes_in_the_Abyss') # Установка заголовка окна

# Инициализация игрового времени
clock = pygame.time.Clock()

# Группы спрайтов
all_sprites = pygame.sprite.Group() # Группа для всех спрайтов в игре
tiles_group = pygame.sprite.Group() # Группа для спрайтов тайлов
player_group = pygame.sprite.Group() # Группа для спрайтов игрока
# Класс камеры
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

def clear_screen():
    for sprite in all_sprites:
        sprite.kill()

def start_game(level_filename, game_over):
    """
    Основной игровой цикл.

    Args:
        player (Player): Объект игрока.
        level (list): Двумерный список, представляющий карту уровня.
    """
    player, level, level_sprites, total_coins = generate_level(level_filename, all_sprites, tiles_group, player_group)
    pygame.mixer.music.load('music/abyss.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    bg = pygame.transform.scale(load_image(BG_IMG), (2*len(level) * TILE_SIZE, 2*len(level[0])  * TILE_SIZE)) # Загрузка и масштабирование фонового изображения
    camera = Camera(WIDTH, HEIGHT)
    running = True # Флаг для управления игровым циклом
    collected_coins = 0
    while running: # Основной игровой цикл
        camera.update(player)
        screen.blit(bg, (0, 0)) # Перерисовываем фон, чтобы скрыть следы от предыдущего положения игрока (можно оптимизировать)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        
        for event in pygame.event.get(): # Обработка событий
            if event.type == pygame.QUIT: # Если событие - закрытие окна
                running = False # Завершаем игровой цикл
            elif event.type == pygame.KEYDOWN: # Если нажата клавиша и игрок не двигается
                if event.key == pygame.K_UP or event.key == pygame.K_w: # Клавиши движения вверх
                    player.move(level, 'up') # Перемещаем игрока вверх
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Клавиши движения вправо
                    player.move(level, 'right') # Перемещаем игрока вправо
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: # Клавиши движения вниз
                    player.move(level, 'down') # Перемещаем игрока вниз
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # Клавиши движения влево
                    player.move(level, 'left') # Перемещаем игрока влево
        x = player.rect.x // TILE_SIZE
        y = player.rect.y // TILE_SIZE
        curr_tile = level[y][x]
        # TODO put this logic in tile class
        if curr_tile == 'c':
            level[y][x] = 'e'
            level_sprites[y][x].kill()
            level_sprites[y][x] = Tile('empty', x, y, [tiles_group, all_sprites])
            collected_coins += 1
        if x == player.rect.x / TILE_SIZE and y == player.rect.y / TILE_SIZE:
            if curr_tile in 'yghj':
                pygame.mixer.music.stop()
                clear_screen()
                game_over(False)
            if curr_tile == 'l':
                player.moving = False
                if player.direction == 'down':
                    player.move(level, 'left')
                elif player.direction == 'up':
                    player.move(level, 'right')
                elif player.direction == 'left':
                    player.move(level, 'down')
                elif player.direction == 'right':
                    player.move(level, 'up')
            elif curr_tile == 'r':
                player.moving = False
                if player.direction == 'down':
                    player.move(level, 'right')
                elif player.direction == 'up':
                    player.move(level, 'left')
                elif player.direction == 'left' :
                    player.move(level, 'up')
                elif player.direction == 'right':
                    player.move(level, 'down')
        if curr_tile == 'f':
            pygame.mixer.music.stop()
            clear_screen()
            game_over(True, collected_coins, total_coins)
        if player.moving: # Если игрок в движении
            player.move(level) # Продолжаем движение в текущем направлении
        else:
            if player.nextmove:
                player.move(level, player.nextmove)
                player.nextmove = None
        camera.update(player)

        pygame.display.flip() # Обновление экрана
        clock.tick(FPS) # Контроль частоты кадров

    terminate() # Завершение игры после выхода из игрового цикла
