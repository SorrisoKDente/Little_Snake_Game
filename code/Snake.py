import pygame.draw
from pygame import Vector2
import os
from code.Const import CELL_SIZE, OFFSET, COLOR_WHITE


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

        try:
            self.eat_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'asset', 'eat.wav'))
            self.game_over_sound = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), '..', 'asset', 'game_over.wav'))
        except pygame.error:
            self.eat_sound = None
            self.game_over_sound = None

    def draw(self, screen):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_WHITE, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body [:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)