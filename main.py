import pygame
import sys
import os
FPS = 50
WIDTH = 800
HEIGHT = 800
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
        self.direction = 'right'
        self.pos = {
            'x': tile_size * pos_x,
            'y': tile_size * pos_y,
        }
        self.moving = False
        self.image = player_image
        self.rect = self.image.get_rect().move(self.pos['x'], self.pos['y'])

    def move(self, direction=None, level=''):
        if direction != None:
            self.direction = direction
        self.moving = True
        if self.direction == 'left':
            if level[(self.pos['x'] - 1) // tile_size][self.pos['y'] // tile_size] == '#':
                self.moving = False
                return
            self.pos['x'] -= 5
        elif self.direction == 'right':
            if level[(self.pos['x']) // tile_size + 1][self.pos['y'] // tile_size] == '#':
                self.moving = False
                return
            self.pos['x'] += 5
        elif self.direction == 'up':
            if level[self.pos['x'] // tile_size][(self.pos['y'] - 1) // tile_size] == '#':
                self.moving = False
                return
            self.pos['y'] -= 5
        elif self.direction == 'down':
            if level[self.pos['x'] // tile_size][self.pos['y'] // tile_size + 1] == '#':
                self.moving = False
                return
            self.pos['y'] += 5
        self.rect = self.image.get_rect().move(self.pos['x'], self.pos['y'])

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
def start_game(player, level):
    bg = pygame.transform.scale(load_image('bg.png'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and not player.moving:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move('up', level)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move('right', level)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move('down', level)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move('left', level)
                screen.blit(bg, player)
        if player.moving:
            player.move(None, level)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Echoes_in_the_Abyss')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_game(*generate_level(load_level('lvl1.txt')))