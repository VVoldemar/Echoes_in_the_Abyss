from config import BG_IMG, WIDTH, HEIGHT, TILE_SIZE, FPS
from button import Button
from utils import get_font, load_image
from utils import tile_to_symbol
from sprites import Tile, Player

import pygame
import sys

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        return obj.rect.move(self.x, self.y)

    def move(self, x, y):
        # Corrected movement logic (we now add)
        self.x += x
        self.y += y


def terminate():
    pygame.quit()
    sys.exit()


def draw_grid(surface, camera):
    """Draws the grid lines on the surface."""
    grid_color = (100, 100, 100)  # Gray color for the grid

    for x in range(-camera.x % TILE_SIZE, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, grid_color, (x + camera.x, 0), (x + camera.x, HEIGHT))
    for y in range(-camera.y % TILE_SIZE, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, grid_color, (0, y + camera.y), (WIDTH, y + camera.y))

camera = Camera(WIDTH, HEIGHT)
def create_level(go_to_main_menu):
    pygame.key.set_repeat(250, 100)
    bg = pygame.transform.scale(load_image(BG_IMG), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    level_matrix = [['e' for _ in range(90)] for _ in range(90)]


    menu_tiles = []
    menu_tile_y = 50

    player = Player(0, 0, [menu_sprites])
    player.rect.x = 20
    player.rect.y = menu_tile_y
    menu_tiles.append(player)
    menu_tile_y += max(player.image.get_height(), TILE_SIZE) + 20

    tile = Tile('wall', 0, 0, [menu_sprites])
    tile.rect.x = 20
    tile.rect.y = menu_tile_y
    menu_tiles.append(tile)
    menu_tile_y += max(tile.image.get_height(), TILE_SIZE) + 20

    trampoline1 = Tile('trampoline', 0, 0, [menu_sprites], direction='l')
    trampoline1.rect.x = 20
    trampoline1.rect.y = menu_tile_y
    menu_tiles.append(trampoline1)
    menu_tile_y += max(trampoline1.image.get_height(), TILE_SIZE) + 20

    trampoline2 = Tile('trampoline', 0, 0, [menu_sprites], direction='r')
    trampoline2.rect.x = 20
    trampoline2.rect.y = menu_tile_y
    menu_tiles.append(trampoline2)
    menu_tile_y += max(trampoline2.image.get_height(), TILE_SIZE) + 20

    finish = Tile('finish', 0, 0, [menu_sprites])
    finish.rect.x = 20
    finish.rect.y = menu_tile_y
    menu_tiles.append(finish)
    menu_tile_y += max(finish.image.get_height(), TILE_SIZE) + 20

    spikes1 = Tile('spikes', 0, 0, [menu_sprites], direction='j')
    spikes1.rect.x = 20
    spikes1.rect.y = menu_tile_y
    menu_tiles.append(spikes1)
    menu_tile_y += max(spikes1.image.get_height(), TILE_SIZE) + 20

    spikes2 = Tile('spikes', 0, 0, [menu_sprites], direction='y')
    spikes2.rect.x = 20
    spikes2.rect.y = menu_tile_y
    menu_tiles.append(spikes2)
    menu_tile_y += max(spikes2.image.get_height(), TILE_SIZE) + 20

    spikes3 = Tile('spikes', 0, 0, [menu_sprites], direction='h')
    spikes3.rect.x = 20
    spikes3.rect.y = menu_tile_y
    menu_tiles.append(spikes3)
    menu_tile_y += max(spikes3.image.get_height(), TILE_SIZE) + 20

    spikes4 = Tile('spikes', 0, 0, [menu_sprites], direction='g')
    spikes4.rect.x = 20
    spikes4.rect.y = menu_tile_y
    menu_tiles.append(spikes4)
    menu_tile_y += max(spikes4.image.get_height(), TILE_SIZE) + 20

    coin = Tile('coin', 0, 0, [menu_sprites])
    coin.rect.x = 20
    coin.rect.y = menu_tile_y
    menu_tiles.append(coin)
    menu_tile_y += max(coin.image.get_height(), TILE_SIZE) + 20

    empty = Tile('empty', 0, 0, [menu_sprites], direction='d')
    empty.rect.x = 20
    empty.rect.y = menu_tile_y
    menu_tiles.append(empty)

    column_count = 6
    tile_x_offset = 20
    tile_y_offset = 50

    for i, tile in enumerate(menu_tiles):
        col = i // column_count
        row = i % column_count
        tile.rect.x = 20 + col * 100
        tile.rect.y = tile_y_offset + row * (max(tile.image.get_height(), TILE_SIZE) + 20)

    tiles_menu = menu_tiles[:]

    current_tile = None
    current_tile_direction = None
    cx, cy = 0, 0
    placing_mode = False
    selected_tile_text = ""
    menu_rect = pygame.Rect(0, 0, 200, HEIGHT)
    menu_color = (150, 150, 150)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        # Draw the grid
        draw_grid(screen, camera)
        save_button = Button(pos=(WIDTH - 300, 50),
                             text_input="SAVE", font=get_font(75), base_color="#06A77D", hovering_color="White")
        save_button.changeColor(mouse_pos)
        save_button.update(screen)

        exit_button = Button(pos=(WIDTH - 100, 50),
                             text_input="EXIT", font=get_font(75),
                             base_color="#06A77D", hovering_color="White")
        exit_button.changeColor(mouse_pos)
        exit_button.update(screen)

        pygame.draw.rect(screen, menu_color, menu_rect)
        selected_tile_surface = get_font(
            30).render(selected_tile_text, True, "White")
        selected_tile_rect = selected_tile_surface.get_rect(
            topleft=(210, 10))
        screen.blit(selected_tile_surface, selected_tile_rect)

        for tile in menu_tiles:
            screen.blit(tile.image, tile.rect)
            if isinstance(tile, Player):
                continue
            tile.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                from gui import main_menu

                if save_button.checkForInput(mouse_pos):
                    save_level(level_matrix)
                    go_to_main_menu()
                if exit_button.checkForInput(mouse_pos):
                    go_to_main_menu()

                if menu_rect.collidepoint(mouse_pos):
                    for tile in menu_tiles:
                        if tile.rect.collidepoint(x, y):
                            if tile.tile_type == 'empty':
                                clear_level(level_matrix, tiles_group, player)
                                break
                            current_tile = tile.tile_type
                            current_tile_direction = None
                            if tile.direction is not None:
                                current_tile_direction = tile.direction
                            selected_tile_text = f"Selected tile: {current_tile}"
                            if current_tile_direction is not None:
                                selected_tile_text += f" ({current_tile_direction})"
                            pygame.mouse.set_cursor(*pygame.cursors.diamond)
                            placing_mode = True
                            break

                elif placing_mode and current_tile:
                    place_tile(level_matrix, current_tile, current_tile_direction, x, y, cx, cy, player,
                               all_sprites, menu_sprites, tiles_group)

                if pygame.mouse.get_pressed()[2]:
                    remove_tile(level_matrix, x, y, cx, cy, tiles_group, player)

            elif event.type == pygame.MOUSEBUTTONUP:
                if placing_mode:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)

            elif event.type == pygame.MOUSEMOTION:
                if placing_mode and current_tile and pygame.mouse.get_pressed()[0]:
                    x, y = event.pos
                    place_tile(level_matrix, current_tile,
                               current_tile_direction, x, y, cx, cy, player, all_sprites, menu_sprites, tiles_group)
                if pygame.mouse.get_pressed()[2]:
                    x, y = event.pos
                    remove_tile(level_matrix, x, y, cx, cy, tiles_group, player)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    camera.move(0, TILE_SIZE)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    camera.move(0, -TILE_SIZE)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    camera.move(TILE_SIZE, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    camera.move(-TILE_SIZE, 0)

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
        with open('./levels/' + filename, 'w') as mapFile:
            for line in level_matrix:
                mapFile.write(''.join(map(str, line)) + '\n')
        file.write('\n' + filename)


def clear_level(level_matrix, tiles_group, player):
    """Clears all tiles from the level."""
    for row in range(len(level_matrix)):
        for col in range(len(level_matrix[0])):
            level_matrix[row][col] = 'e'

    for tile in tiles_group:
        if tile.tile_type == 'player':
            level_matrix[tile.rect.y //
                         TILE_SIZE][tile.rect.x // TILE_SIZE] = 'e'
            player.rect = player.image.get_rect().move(0, TILE_SIZE)
        tile.kill()


def remove_tile(level_matrix, x, y, cx, cy, tiles_group, player):
    """Removes a tile at the given mouse position."""
    grid_x = (x + cx) // TILE_SIZE
    grid_y = (y + cy) // TILE_SIZE

    if 0 <= grid_x < len(level_matrix[0]) and 0 <= grid_y < len(level_matrix):
        if level_matrix[grid_y][grid_x] == 'p':
            level_matrix[grid_y][grid_x] = 'e'
            player.rect = player.image.get_rect().move(0, TILE_SIZE)

        for tile in tiles_group:
            if tile.rect.x == grid_x * TILE_SIZE and tile.rect.y == grid_y * TILE_SIZE:
                tile.kill()
                level_matrix[grid_y][grid_x] = 'e'
                break


def place_tile(level_matrix, current_tile, current_tile_direction, x, y, cx, cy, player, all_sprites, menu_sprites, tiles_group):
    """Places a tile on the level grid, handling player and other tiles."""
    if current_tile is None:
        return

    grid_x = (x - camera.x) // TILE_SIZE
    grid_y = (y - camera.y) // TILE_SIZE

    if not (0 <= grid_x < len(level_matrix[0]) and 0 <= grid_y < len(level_matrix)):
        return

    # Remove tile
    for tile in tiles_group:
        if tile.rect.x == grid_x * TILE_SIZE and tile.rect.y == grid_y * TILE_SIZE:
            tile.kill()
            break

    if current_tile == 'player':
        level_matrix[player.rect.y // TILE_SIZE][player.rect.x // TILE_SIZE] = 'e'

        level_matrix[grid_y][grid_x] = 'p'
        player.rect.x = grid_x * TILE_SIZE
        player.rect.y = grid_y * TILE_SIZE

        menu_sprites.remove(player)

    else:
        if current_tile_direction is not None:
            level_matrix[grid_y][grid_x] = tile_to_symbol[current_tile + current_tile_direction]
        else:
            level_matrix[grid_y][grid_x] = tile_to_symbol[current_tile]

        Tile(current_tile, grid_x, grid_y, [tiles_group, all_sprites], direction=current_tile_direction)

def remove_tile(level_matrix, x, y, cx, cy, tiles_group, player):
    """Removes a tile at the given mouse position."""
    grid_x = (x - cx) // TILE_SIZE
    grid_y = (y - cy) // TILE_SIZE

    if 0 <= grid_x < len(level_matrix[0]) and 0 <= grid_y < len(level_matrix):
        if level_matrix[grid_y][grid_x] == 'p':
            level_matrix[grid_y][grid_x] = 'e'
            player.kill()
            player.rect = player.image.get_rect().move(0, TILE_SIZE)

        for tile in tiles_group:
            if tile.rect.x == grid_x * TILE_SIZE and tile.rect.y == grid_y * TILE_SIZE:
                tile.kill()
                level_matrix[grid_y][grid_x] = 'e'
                break

if __name__ == '__main__':
    pygame.init()
    # pygame.key.set_repeat(500, 30)
    pygame.display.set_caption('Echoes_in_the_Abyss')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    from gui import main_menu
    create_level(main_menu)