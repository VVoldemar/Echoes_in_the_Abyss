from config import BG_IMG, WIDTH, HEIGHT, TILE_SIZE, FPS
from button import Button
from utils import get_font, load_image
from utils import Camera, tile_to_symbol
from sprites import Tile, Player

import pygame
import sys
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


all_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def create_level():
    pygame.key.set_repeat(500, 30)
    bg = pygame.transform.scale(load_image(BG_IMG), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    level_matrix = [['e' for _ in range(90)] for _ in range(90)]
    player = Player(0, 1, [menu_sprites])
    tile = Tile('wall', 1, 1, [menu_sprites])
    trampoline1 = Tile('trampoline', 2, 1, [menu_sprites], direction='l')
    trampoline2 = Tile('trampoline', 2, 2, [menu_sprites], direction='r')
    finish = Tile('finish', 3, 1, [menu_sprites])
    spikes1 = Tile('spikes', 4, 1, [menu_sprites], direction='j')
    spikes2 = Tile('spikes', 4, 2, [menu_sprites], direction='y')
    spikes3 = Tile('spikes', 5, 1, [menu_sprites], direction='h')
    spikes4 = Tile('spikes', 5, 2, [menu_sprites], direction='g')
    coin = Tile('coin', 6, 1, [menu_sprites])
    empty = Tile('empty', 7, 1, [menu_sprites], direction='d')
    tiles_menu = [player, tile, trampoline1, trampoline2,
                  finish, spikes1, spikes2, spikes3, spikes4, coin, empty]
    current_tile = None
    cx, cy = 0, 0
    camera = Camera(WIDTH, HEIGHT)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        save_button = Button(pos=(WIDTH-100, 50),
                             text_input="SAVE", font=get_font(75), base_color="#06A77D", hovering_color="White")
        save_button.changeColor(mouse_pos)
        save_button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if save_button.checkForInput(mouse_pos):
                    save_level(level_matrix)
                    terminate()
                for tile in tiles_menu:
                    if tile.rect.collidepoint(x, y):
                        current_tile = tile.tile_type
                        current_tile_direction = None
                        if tile.direction is not None:
                            current_tile_direction = tile.direction
                        pygame.mouse.set_cursor(*pygame.cursors.diamond)
                        break
                    elif current_tile != None:
                        x += cx
                        y += cy
                        if current_tile == 'player':
                            level_matrix[player.rect.y //
                                         TILE_SIZE][player.rect.x // TILE_SIZE] = 'e'
                            level_matrix[y // TILE_SIZE][x // TILE_SIZE] = 'p'
                            player.rect = player.image.get_rect().move(
                                x // TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE)
                            all_sprites.add(player)
                            menu_sprites.remove(player)
                        else:
                            if current_tile_direction != None:
                                level_matrix[y // TILE_SIZE][x //
                                                             TILE_SIZE] = tile_to_symbol[current_tile + current_tile_direction]
                            else:
                                level_matrix[y // TILE_SIZE][x //
                                                             TILE_SIZE] = tile_to_symbol[current_tile]
                            if current_tile_direction == 'd':
                                current_tile_direction = None
                            Tile(current_tile, x // TILE_SIZE, y //
                                 TILE_SIZE, [tiles_group, all_sprites], direction=current_tile_direction)
                        current_tile = None
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w and cy > 0 and cy < 80 * TILE_SIZE:
                    cy -= 5
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and cx >= 0 and cx < 80 * TILE_SIZE:
                    cx += 5
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s and cy >= 0 and cy < 80 * TILE_SIZE:
                    cy += 5
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a and cx > 0 and cx < 80 * TILE_SIZE:
                    cx -= 5

        menu_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        camera.move(cx, cy)


def save_level(level_matrix):
    """
    Сохраняет уровень в текстовый файл.

    Args:
        level_matrix (list): Двумерный список, представляющий карту уровня.

    """
    levels = []
    with open('./levels/lvllist.txt', 'r') as file:
        for line in file:
            levels.append(line.strip())
    with open('./levels/lvllist.txt', 'a') as file:
        filename = f'lvl{len(levels) + 1}.txt'
        with open(filename, 'w') as mapFile:
            for line in level_matrix:
                mapFile.write(''.join(map(str, line)) + '\n')
        file.write('\n' + filename)


if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(500, 30)
    pygame.display.set_caption('Echoes_in_the_Abyss')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    create_level()
