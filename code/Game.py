import sys

import pygame
from pygame import Vector2
pygame.init()

from code.Const import WIN_WIDTH, WIN_HEIGHT, FPS, COLOR_GREEN, COLOR_BLACK, CELL_SIZE, CELL_NUMBER, SPEED, MOVE_DOWN, \
    MOVE_UP, MOVE_RIGHT, MOVE_LEFT, OFFSET, BORDER_SIZE, FONT_TITLE, COLOR_WHITE, FONT_SCORE
from code.Food import Food
from code.Snake import Snake



class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = 'RUNNING'
        self.score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == 'RUNNING':
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1

    def check_collision_with_edges(self):
        if self.snake.body[0].x == CELL_NUMBER or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == CELL_NUMBER or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = 'STOPPED'
        self.score = 0

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2* OFFSET + CELL_SIZE * CELL_NUMBER , 2* OFFSET + CELL_SIZE * CELL_NUMBER))

pygame.display.set_caption('蛇ちゃんゲーム🐍')

clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, SPEED)

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.state == 'STOPPED':
                game.state = 'RUNNING'

            if event.key == pygame.K_UP and game.snake.direction != MOVE_DOWN:
                game.snake.direction = MOVE_UP
            if event.key == pygame.K_DOWN and game.snake.direction != MOVE_UP:
                game.snake.direction = MOVE_DOWN
            if event.key == pygame.K_LEFT and game.snake.direction != MOVE_RIGHT:
                game.snake.direction = MOVE_LEFT
            if event.key == pygame.K_RIGHT and game.snake.direction != MOVE_LEFT:
                game.snake.direction = MOVE_RIGHT

    # drawing
    screen.fill(COLOR_BLACK)
    pygame.draw.rect(screen, COLOR_WHITE, (OFFSET - BORDER_SIZE, OFFSET - BORDER_SIZE, CELL_SIZE * CELL_NUMBER + 10, CELL_SIZE * CELL_NUMBER + 10), BORDER_SIZE)
    game.draw()
    title_surface = FONT_TITLE.render('蛇ちゃんゲーム', True, COLOR_WHITE)
    score_surface = FONT_SCORE.render(f'SCORE: {str(game.score)}', True, COLOR_WHITE)
    screen.blit(title_surface, (OFFSET - 5, 20))
    screen.blit(score_surface, (OFFSET - 5, OFFSET + CELL_SIZE * CELL_NUMBER + 10))

    pygame.display.update()
    clock.tick(FPS)

