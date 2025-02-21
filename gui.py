import pygame
import sys
from button import Button
from config import BG_IMG, WIDTH, HEIGHT
from editor import create_level
from main import start_game
from utils import get_font, load_image, terminate

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes in the Abyss")

# Загрузка и масштабирование фонового изображения
bg = pygame.transform.scale(load_image(BG_IMG), (WIDTH, HEIGHT))





def level_select():
    levels = []
    with open('./levels/lvllist.txt', 'r') as file:
        for line in file:
            levels.append(line.strip())
    level_buttons = []
    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill("black")

        OPTIONS_TEXT = get_font(45).render("Select level.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        for i in range(len(levels)):
            level_buttons.append(Button(pos=(400+i*50, 350),
                                        text_input=str(i + 1), font=get_font(75), base_color="#06A77D", hovering_color="White"))
        button_back = Button(pos=(WIDTH//2, 660),
                             text_input="BACK", font=get_font(75), base_color="#06A77D", hovering_color="White")

        button_back.changeColor(mouse_pos)
        button_back.update(screen)
        for btn in level_buttons:
            btn.changeColor(mouse_pos)
            btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in level_buttons:
                    if btn.checkForInput(mouse_pos):
                        start_game(levels[int(btn.text_input) - 1], game_over)
                if button_back.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()


def game_over(win, collected_coins=0, total_coins=0):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))
        if win:
            text = get_font(45).render(
                f"Level completed. {collected_coins} / {total_coins} coins", True, "#06A77D")
            text_rect = text.get_rect(center=(WIDTH//2, 260))
        else:
            text = get_font(45).render("Game over.", True, "#06A77D")
            text_rect = text.get_rect(center=(WIDTH//2, 260))
        screen.blit(text, text_rect)
        back_to_levels = Button(pos=(WIDTH//2, 460),
                                text_input="BACK TO LEVELS", font=get_font(75), base_color="#06A77D", hovering_color="White")

        back_to_levels.changeColor(mouse_pos)
        back_to_levels.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_levels.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(WIDTH//2, 100))

        play_button = Button(pos=(WIDTH//2, 250),
                             text_input="PLAY", font=get_font(75), base_color="#06A77D", hovering_color="White")
        editor_button = Button(pos=(WIDTH//2, 400),
                               text_input="EDITOR", font=get_font(75), base_color="#06A77D", hovering_color="White")
        quit_button = Button(pos=(WIDTH//2, 550),
                             text_input="QUIT", font=get_font(75), base_color="#06A77D", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, editor_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    level_select()
                if editor_button.checkForInput(mouse_pos):
                    create_level()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
