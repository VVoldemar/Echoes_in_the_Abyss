import pygame
import sys
from config import TILE_SIZE, WIDTH, HEIGHT, FPS, LEVEL_FILE # Импортируем константы из config.py
from utils import load_image # Импортируем функцию загрузки изображений
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

def terminate():
    """
    Завершает игру.
    """
    pygame.quit()
    sys.exit()

def start_game(player, level):
    """
    Основной игровой цикл.

    Args:
        player (Player): Объект игрока.
        level (list): Двумерный список, представляющий карту уровня.
    """
    bg = pygame.transform.scale(load_image('bg.png'), (WIDTH, HEIGHT)) # Загрузка и масштабирование фонового изображения
    screen.blit(bg, (0, 0)) # Отображение фона на экране
    camera = Camera(WIDTH, HEIGHT)
    running = True # Флаг для управления игровым циклом
    while running: # Основной игровой цикл
        camera.update(player)
        screen.blit(bg, (0, 0)) # Перерисовываем фон, чтобы скрыть следы от предыдущего положения игрока (можно оптимизировать)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        
        for event in pygame.event.get(): # Обработка событий
            if event.type == pygame.QUIT: # Если событие - закрытие окна
                running = False # Завершаем игровой цикл
            elif event.type == pygame.KEYDOWN and not player.moving: # Если нажата клавиша и игрок не двигается
                if event.key == pygame.K_UP or event.key == pygame.K_w: # Клавиши движения вверх
                    player.move(level, 'up') # Перемещаем игрока вверх
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Клавиши движения вправо
                    player.move(level, 'right') # Перемещаем игрока вправо
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: # Клавиши движения вниз
                    player.move(level, 'down') # Перемещаем игрока вниз
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # Клавиши движения влево
                    player.move(level, 'left') # Перемещаем игрока влево
        curr_tile = level[player.rect.y // TILE_SIZE][player.rect.x // TILE_SIZE]
        # TODO put this logic in tile class
        if player.rect.x // TILE_SIZE == player.rect.x / TILE_SIZE and player.rect.y // TILE_SIZE == player.rect.y / TILE_SIZE:
            if curr_tile == 'l':
                if player.direction == 'down':
                    player.move(level, 'left')
                elif player.direction == 'up':
                    player.move(level, 'right')
                elif player.direction == 'left':
                    player.move(level, 'down')
                elif player.direction == 'right':
                    player.move(level, 'up')
            elif curr_tile == 'r' :
                if player.direction == 'down':
                    player.move(level, 'right')
                elif player.direction == 'up':
                    player.move(level, 'left')
                elif player.direction == 'left' :
                    player.move(level, 'up')
                elif player.direction == 'right':
                    player.move(level, 'down')
        if curr_tile == 'f':
            #end_game()
            pass
        if player.moving: # Если игрок в движении
            player.move(level) # Продолжаем движение в текущем направлении
        camera.update(player)

        pygame.display.flip() # Обновление экрана
        clock.tick(FPS) # Контроль частоты кадров

    terminate() # Завершение игры после выхода из игрового цикла

if __name__ == '__main__':
    # Запуск игры при запуске файла main.py
    start_game(*generate_level(LEVEL_FILE, all_sprites, tiles_group, player_group))