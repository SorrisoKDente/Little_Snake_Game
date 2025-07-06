import pygame
import sys
from code.Game import Game
from code.Const import WIN_WIDTH, WIN_HEIGHT, FONT_TITLE, COLOR_WHITE

# Função para desenhar o menu
def draw_menu(screen):
    # Título centralizado
    title_surface = FONT_TITLE.render("蛇ちゃんゲーム", True, COLOR_WHITE)
    title_width, title_height = title_surface.get_size()
    title_x = (screen.get_width() - title_width) // 2
    title_y = screen.get_height() // 4  # Coloca o título um pouco abaixo do topo
    screen.blit(title_surface, (title_x, title_y))

    # Opções de menu
    font = pygame.font.Font(None, 40)
    play_text = font.render("Play", True, COLOR_WHITE)
    play_width, play_height = play_text.get_size()
    play_x = (screen.get_width() - play_width) // 2
    play_y = title_y + 100  # Distância para a opção Play
    screen.blit(play_text, (play_x, play_y))

    exit_text = font.render("Exit", True, COLOR_WHITE)
    exit_width, exit_height = exit_text.get_size()
    exit_x = (screen.get_width() - exit_width) // 2
    exit_y = play_y + 60  # Distância para a opção Exit
    screen.blit(exit_text, (exit_x, exit_y))

    pygame.display.update()

# Função para lidar com a navegação do menu
def menu_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Menu - 蛇ちゃんゲーム🐍')

    clock = pygame.time.Clock()

    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Play
                    game = Game()  # Chama a classe do jogo
                    game_loop(game, screen)
                    menu_active = False

                elif event.key == pygame.K_ESCAPE:  # Exit
                    pygame.quit()
                    sys.exit()

        # Desenhar o menu
        screen.fill((0, 0, 0))  # Fundo preto
        draw_menu(screen)

        clock.tick(60)

# Função para rodar o jogo
def game_loop(game, screen):
    clock = pygame.time.Clock()
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction != game.MOVE_DOWN:
                    game.snake.direction = game.MOVE_UP
                elif event.key == pygame.K_DOWN and game.snake.direction != game.MOVE_UP:
                    game.snake.direction = game.MOVE_DOWN
                elif event.key == pygame.K_LEFT and game.snake.direction != game.MOVE_RIGHT:
                    game.snake.direction = game.MOVE_LEFT
                elif event.key == pygame.K_RIGHT and game.snake.direction != game.MOVE_LEFT:
                    game.snake.direction = game.MOVE_RIGHT

        game.update()

        # Desenhar o jogo
        screen.fill((0, 0, 0))
        game.draw()
        pygame.display.update()
        clock.tick(60)

