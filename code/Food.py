import random

import pygame
from pygame import Vector2

from code.Const import CELL_SIZE, COLOR_D_GREEN, CELL_NUMBER, OFFSET

food_surface = pygame.image.load('../asset/Apple.png')

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        from code.Game import screen
        food_rect = pygame.Rect(OFFSET + self.position.x * CELL_SIZE, OFFSET + self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, CELL_NUMBER -1)
        y = random.randint(0, CELL_NUMBER -1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position