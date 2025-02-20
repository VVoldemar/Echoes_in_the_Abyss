# TODO split this to modules
from config import BG_IMG, WIDTH, HEIGHT, TILE_SIZE, FPS # Импортируем константы из config.py
from utils import load_level, load_image, tile_to_sybmol # Импортируем функцию загрузки уровня
from sprites import Tile, Player # Импортируем классы Tile и Player

import pygame
import sys
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()
    
#начало игры
def create_level():
    bg = pygame.transform.scale(load_image(BG_IMG), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    level_matrix = [['e' for _ in range(30)] for _ in range(30)]
    player = Player(2, 10, [player_group, all_sprites])
    tile = Tile('wall', 3, 10, [tiles_group, all_sprites])
    trampoline = Tile('trampoline', 4, 10, [tiles_group, all_sprites])
    finish = Tile('finish', 5, 10, [tiles_group, all_sprites])
    spikes = Tile('spikes', 6, 10, [tiles_group, all_sprites])
    coin = Tile('coin', 6, 10, [tiles_group, all_sprites])
    tiles_menu = [player, tile, trampoline, finish, spikes, coin]
    current_tile = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    save_level(level_matrix)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for tile in tiles_menu:
                    if tile.rect.collidepoint(x, y):
                        current_tile = tile.tile_type
                        pygame.mouse.set_cursor(*pygame.cursors.diamond)
                        break
                    elif current_tile != None:
                        if current_tile == 'player':
                            level_matrix[player.rect.y // TILE_SIZE][player.rect.x // TILE_SIZE] = 'e'
                            level_matrix[y // TILE_SIZE][x // TILE_SIZE] = 'p'
                            player.rect = player.image.get_rect().move(x // TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE)
                        else:
                            level_matrix[y // TILE_SIZE][x // TILE_SIZE] = tile_to_sybmol[current_tile]
                            Tile(current_tile, x // TILE_SIZE, y // TILE_SIZE, [tiles_group, all_sprites])
                        current_tile = None
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)

            screen.blit(bg, (0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def save_level(level_matrix):
    """
    Сохраняет уровень в текстовый файл.

    Args:
        level_matrix (list): Двумерный список, представляющий карту уровня.

    """
    filename = "levels/" + 'lvl2.txt'  # Формируем путь к файлу уровня
    with open(filename, 'w') as mapFile:
        for line in level_matrix:
            mapFile.write(''.join(map(str, line)) + '\n')


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Echoes_in_the_Abyss')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    create_level()
