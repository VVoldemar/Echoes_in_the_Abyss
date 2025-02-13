# TODO split this to modules
from config import WIDTH, HEIGHT, FPS # Импортируем константы из config.py
from utils import load_level # Импортируем функцию загрузки уровня
import pygame
import sys
import os
clock = pygame.time.Clock()
#функция загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('empty.png'),
}
player_image = load_image('player.png')

tile_size = 50

#функция загрузки уровня
def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

#класс поля
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)

#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)
   

#генереция уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y).rect
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, level

def terminate():
    pygame.quit()
    sys.exit()
    
#начало игры
def create_level():
    bg = pygame.transform.scale(load_image('bg.png'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    player = Player(2, 10)
    tile = Tile('wall', 3, 10)
    current_tile = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if player.rect.collidepoint(x, y):
                    current_tile = 'player'
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                elif tile.rect.collidepoint(x, y):
                    current_tile = 'tile'
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                elif current_tile != None:
                    if current_tile == 'player':
                        player.rect = player.image.get_rect().move(x // tile_size * tile_size, y // tile_size * tile_size)
                    elif current_tile == 'tile':
                        Tile('wall', x // tile_size, y // tile_size)
                    current_tile = None
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)

            screen.blit(bg, (0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Echoes_in_the_Abyss')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    create_level()
