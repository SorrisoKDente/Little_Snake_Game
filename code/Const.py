import pygame, os
from pygame import Vector2
pygame.font.init()
font_path = os.path.join(os.path.dirname(__file__), '..', 'asset', 'NotoSansJP.ttf')


# B
BORDER_SIZE = 5

# C
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (173, 204, 96)
COLOR_D_GREEN = (43, 51, 24)
CELL_SIZE = 20
CELL_NUMBER = 20

# F
FONT_TITLE = pygame.font.Font(font_path, 30)
FONT_TITLE_MENU = pygame.font.Font(font_path, 45)
FONT_OPTION = pygame.font.Font(None, 40)
FONT_SCORE = pygame.font.Font(None, 30)
FPS = 60

# M
MENU_OPTION = ('Play',
               'Exit')

MOVE_DOWN = Vector2(0, 1)
MOVE_LEFT = Vector2(-1, 0)
MOVE_RIGHT = Vector2(1, 0)
MOVE_UP = Vector2(0, -1)

# O
OFFSET = 75

# S
SPEED = 100


# W
WIN_WIDTH = CELL_SIZE * CELL_NUMBER
WIN_HEIGHT = CELL_SIZE * CELL_NUMBER