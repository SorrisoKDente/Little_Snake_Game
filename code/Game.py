import sys, pygame, os

from code.Score import save_score

pygame.init()
pygame.mixer.init()

from code.Const import FPS, COLOR_BLACK, CELL_SIZE, CELL_NUMBER, SPEED, MOVE_DOWN, \
    MOVE_UP, MOVE_RIGHT, MOVE_LEFT, OFFSET, BORDER_SIZE, FONT_TITLE, COLOR_WHITE, FONT_SCORE, \
    COLOR_GREEN, FONT_OPTION, PAUSE_OPTION
from code.Food import Food
from code.Snake import Snake


def draw_confirmation_dialog(screen, message, selection): # Adicionado o parâmetro 'selection'
    # Desenha o fundo do diálogo
    dialog_width = 400
    dialog_height = 200
    dialog_x = (screen.get_width() - dialog_width) // 2
    dialog_y = (screen.get_height() - dialog_height) // 2

    # Fundo do diálogo
    pygame.draw.rect(screen, COLOR_BLACK, (dialog_x, dialog_y, dialog_width, dialog_height))
    pygame.draw.rect(screen, COLOR_WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

    # Mensagem
    msg_surface = FONT_OPTION.render(message, True, COLOR_WHITE)
    msg_rect = msg_surface.get_rect(center=(screen.get_width() // 2, dialog_y + 60))
    screen.blit(msg_surface, msg_rect)

    # Cores dinâmicas baseadas na seleção
    # Se selection for 1 (YES), fica verde. Se for 0 (NO), fica branco.
    yes_color = COLOR_GREEN if selection == 1 else COLOR_WHITE
    no_color = COLOR_GREEN if selection == 0 else COLOR_WHITE

    yes_surface = FONT_OPTION.render('YES', True, yes_color)
    no_surface = FONT_OPTION.render('NO', True, no_color)

    yes_rect = yes_surface.get_rect(center=(screen.get_width() // 2 - 80, dialog_y + 130))
    no_rect = no_surface.get_rect(center=(screen.get_width() // 2 + 80, dialog_y + 130))

    screen.blit(yes_surface, yes_rect)
    screen.blit(no_surface, no_rect)

    # Instruções
    instructions = FONT_SCORE.render('Use LEFT/RIGHT to choose, ENTER to confirm', True, COLOR_GREEN)
    instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, dialog_y + 170))
    screen.blit(instructions, instructions_rect)

    return yes_rect, no_rect


def handle_quit_game():
    """Sai do jogo completamente"""
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self, return_to_menu_callback=None):  # Adicione este parâmetro
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = 'RUNNING'
        self.score = 0

        try:
            self.bg_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'asset', 'bg_sound.mp3'))
            self.pause_selection_sound = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), '..', 'asset', 'option.wav'))
            self.confirm_sound = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), '..', 'asset', 'select.wav'))
            if self.bg_sound: self.bg_sound.play(-1)
        except pygame.error:
            print("Aviso: Áudio do jogo indisponível.")
            self.bg_sound = None
            self.pause_selection_sound = None
            self.confirm_sound = None

        # Adicione essas variáveis para controle do menu de pausa
        self.pause_menu_option = 0

        # Callback para retornar ao menu
        self.return_to_menu_callback = return_to_menu_callback

    def draw(self, screen):
        self.food.draw(screen)
        self.snake.draw(screen)

        score_surface = FONT_SCORE.render(f'SCORE: {str(self.score)}', True, COLOR_WHITE)
        screen.blit(score_surface, (OFFSET - 5, OFFSET + CELL_SIZE * CELL_NUMBER + 10))

    def draw_pause_menu(self, screen):
        # Desenha um overlay semi-transparente
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Preto semi-transparente
        screen.blit(overlay, (0, 0))

        # Desenha o título do menu de pausa
        pause_title = FONT_TITLE.render('GAME PAUSED', True, COLOR_WHITE)
        pause_rect = pause_title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(pause_title, pause_rect)

        # Desenha as opções do menu
        for i, option in enumerate(PAUSE_OPTION):
            color = COLOR_GREEN if i == self.pause_menu_option else COLOR_WHITE
            option_surface = FONT_OPTION.render(option, True, color)
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2,
                                                          screen.get_height() // 2 + i * 50))
            screen.blit(option_surface, option_rect)

        # Instruções
        instructions = FONT_SCORE.render('Press ESC to resume', True, COLOR_GREEN)
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2,
                                                          screen.get_height() - 50))
        screen.blit(instructions, instructions_rect)

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
            self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == CELL_NUMBER or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == CELL_NUMBER or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        save_score(self.score)

        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = 'STOPPED'
        self.score = 0
        self.snake.game_over_sound.play()
        self.bg_sound.stop()

    def game_restart(self):
        self.bg_sound.play(-1)

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def run(self):
        screen = pygame.display.set_mode((2 * OFFSET + CELL_SIZE * CELL_NUMBER, 2 * OFFSET + CELL_SIZE * CELL_NUMBER))
        pygame.display.set_caption('蛇ちゃんゲーム🐍')
        clock = pygame.time.Clock()

        snake_update = pygame.USEREVENT
        pygame.time.set_timer(snake_update, SPEED)

        # Estados adicionais para controle do menu
        in_pause_menu = False
        in_confirmation = False
        confirmation_type = ""
        confirmation_callback = None
        confirmation_selection = 0  # 0 = NO, 1 = YES
        should_exit_to_menu = False

        while True:
            for event in pygame.event.get():
                if event.type == snake_update:
                    if not in_pause_menu and not in_confirmation:
                        self.update()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        if not in_confirmation:
                            in_pause_menu = not in_pause_menu
                            self.pause_selection_sound.play()

                    # Navegação no menu de pausa
                    elif in_pause_menu and not in_confirmation:
                        # Navegação do menu de pausa (UP/DOWN)
                        if event.key == pygame.K_DOWN:
                            self.pause_menu_option = (self.pause_menu_option + 1) % len(PAUSE_OPTION)
                            self.pause_selection_sound.play()
                        elif event.key == pygame.K_UP:
                            self.pause_menu_option = (self.pause_menu_option - 1) % len(PAUSE_OPTION)
                            self.pause_selection_sound.play()

                        elif event.key == pygame.K_RETURN:
                            self.confirm_sound.play()
                            option = PAUSE_OPTION[self.pause_menu_option]
                            if option == 'Resume':
                                in_pause_menu = False
                            else:
                                in_confirmation = True
                                confirmation_type = option
                                confirmation_selection = 0

                    elif in_confirmation:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            confirmation_selection = 1 - confirmation_selection
                            self.pause_selection_sound.play()

                        elif event.key == pygame.K_RETURN:
                            self.confirm_sound.play()
                            if confirmation_selection == 1:  # Escolheu YES
                                if confirmation_type == 'Back to Menu':
                                    self.bg_sound.stop()
                                    return True  # Retorna para o Menu.py
                                elif confirmation_type == 'Quit Game':
                                    pygame.quit()
                                    sys.exit()
                            else:  # Escolheu NO
                                in_confirmation = False

                    # Navegação no diálogo de confirmação
                    elif in_confirmation:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            confirmation_selection = 1 - confirmation_selection  # Alterna entre 0 e 1
                            self.pause_selection_sound.play()

                        elif event.key == pygame.K_RETURN:
                            self.confirm_sound.play()
                            if confirmation_selection == 1:  # YES
                                # Salva o score antes de sair
                                if self.score > 0:
                                    save_score(self.score)
                                confirmation_callback()
                                return should_exit_to_menu  # Retorna True se for voltar ao menu
                            else:  # NO
                                in_confirmation = False

                    # Controles do jogo (apenas quando não está em menu)
                    elif not in_pause_menu and not in_confirmation:
                        if self.state == 'STOPPED':
                            self.state = 'RUNNING'
                            self.game_restart()

                        if event.key == pygame.K_UP and self.snake.direction != MOVE_DOWN:
                            self.snake.direction = MOVE_UP
                        if event.key == pygame.K_DOWN and self.snake.direction != MOVE_UP:
                            self.snake.direction = MOVE_DOWN
                        if event.key == pygame.K_LEFT and self.snake.direction != MOVE_RIGHT:
                            self.snake.direction = MOVE_LEFT
                        if event.key == pygame.K_RIGHT and self.snake.direction != MOVE_LEFT:
                            self.snake.direction = MOVE_RIGHT

            # Verifica se precisa retornar ao menu
            if should_exit_to_menu:
                return True  # Retorna True para indicar que deve voltar ao menu

            # Desenhar
            screen.fill(COLOR_BLACK)
            pygame.draw.rect(screen, COLOR_WHITE, (OFFSET - BORDER_SIZE, OFFSET - BORDER_SIZE,
                                                   CELL_SIZE * CELL_NUMBER + 10, CELL_SIZE * CELL_NUMBER + 10),
                             BORDER_SIZE)
            self.draw(screen)
            title_surface = FONT_TITLE.render('蛇ちゃんゲーム', True, COLOR_WHITE)
            score_surface = FONT_SCORE.render(f'SCORE: {str(self.score)}', True, COLOR_WHITE)
            screen.blit(title_surface, (OFFSET - 5, 20))
            screen.blit(score_surface, (OFFSET - 5, OFFSET + CELL_SIZE * CELL_NUMBER + 10))

            # Desenhar menu de pausa se necessário
            if in_pause_menu:
                self.draw_pause_menu(screen)
                if in_confirmation:
                    msg = "Back to Menu?" if confirmation_type == 'Back to Menu' else "Quit Game?"
                    draw_confirmation_dialog(screen, msg, confirmation_selection)

            pygame.display.update()
            clock.tick(FPS)

    def handle_back_to_menu(self):
        """Marca para voltar ao menu principal"""
        self.bg_sound.stop()
        return True

