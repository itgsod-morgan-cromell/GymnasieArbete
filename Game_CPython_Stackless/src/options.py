import pygame

pygame.init()
WIDTH = int(1240 / 64) * 64
HEIGHT = int(700 / 64) * 64
MENU_WIDTH = int(300 / 64) * 64
CONSOLE_HEIGHT = int((HEIGHT/4)/64) * 64
SCALE = 1
ALWAYS_SHOW_STATS = True
CONSOLE_FONT_SIZE = 14
TOOLTIP_FONT_SIZE = 20
common = (255, 255, 255)
uncommon = (30, 255, 0)
rare = (0, 112, 255)
epic = (163, 53, 238)
cursor = pygame.image.load('../res/gui/cursor.png')
cursor_green = pygame.image.load('../res/gui/cursor_green.png')
cursor_red = pygame.image.load('../res/gui/cursor_red.png')

CONSOLE_FONT = pygame.font.Font('../res/other/veramono.ttf', CONSOLE_FONT_SIZE)
INTERFACE_COLOR = (54, 54, 54)
INTERFACE_Y = 300



