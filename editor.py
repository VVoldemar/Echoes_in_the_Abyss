# TODO split this to modules
from config import WIDTH, HEIGHT, TILE_SIZE, FPS # Импортируем константы из config.py
from utils import load_level # Импортируем функцию загрузки уровня
from sprites import Tile, Player # Импортируем классы Tile и Player

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


player_image = load_image('player.png')


def terminate():
    pygame.quit()
    sys.exit()
    
#начало игры
def create_level():
    bg = pygame.transform.scale(load_image('bg.png'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    player = Player(2, 10, [player_group, all_sprites])
    tile = Tile('wall', 3, 10, [tiles_group, all_sprites])
    trampoline = Tile('trampoline', 4, 10, [tiles_group, all_sprites])
    finish = Tile('finish', 5, 10, [tiles_group, all_sprites])

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
                        player.rect = player.image.get_rect().move(x // TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE)
                    elif current_tile == 'tile':
                        Tile('wall', x // TILE_SIZE, y // TILE_SIZE, [tiles_group, all_sprites])
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
