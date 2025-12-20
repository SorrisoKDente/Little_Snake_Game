import pygame, sys, os

from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_BLACK, FONT_TITLE_MENU, COLOR_WHITE, COLOR_GREEN, FONT_OPTION, FPS, \
    MENU_OPTION
from code.Game import Game
from code.Score import load_scores

pygame.init()


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('蛇ちゃんゲーム Game Menu')
        self.option_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'asset', 'option.wav'))
        self.select_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'asset', 'select.wav'))
        self.menu_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'asset', 'menu_sound.ogg'))

        # Variáveis para controle de confirmação
        self.in_confirmation = False
        self.confirmation_selection = 0  # 0 = NO, 1 = YES
        self.confirmation_target = None  # Qual opção está sendo confirmada

        # Inicia o som do menu
        self.start_menu_sound()

    def start_menu_sound(self):
        """Inicia o som do menu"""
        if not self.menu_sound.get_num_channels():
            self.menu_sound.play(-1)

    def show_scores(self):
        self.screen.fill(COLOR_BLACK)

        scores = load_scores()

        self.screen.fill(COLOR_BLACK)
        title_surface = FONT_TITLE_MENU.render('Top 5 Scores', True, COLOR_WHITE)
        title_rect = title_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4))
        self.screen.blit(title_surface, title_rect)

        score_font = pygame.font.SysFont("Lucida Sans Typewriter", 30)

        for idx, score in enumerate(scores):
            score_text = f"{idx + 1}° Place - {score} Points"
            score_surface = score_font.render(score_text, True, COLOR_WHITE)
            score_rect = score_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + idx * 30))
            self.screen.blit(score_surface, score_rect)

        back_text = "Press ENTER to return"
        back_surface = FONT_OPTION.render(back_text, True, COLOR_GREEN)
        back_rect = back_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
        self.screen.blit(back_surface, back_rect)

        pygame.display.update()

    def draw_confirmation_dialog(self, message):
        # Desenha o fundo do diálogo
        dialog_width = 400
        dialog_height = 200
        dialog_x = (self.screen.get_width() - dialog_width) // 2
        dialog_y = (self.screen.get_height() - dialog_height) // 2

        # Fundo do diálogo
        pygame.draw.rect(self.screen, COLOR_BLACK, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, COLOR_WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # Mensagem
        msg_surface = FONT_OPTION.render(message, True, COLOR_WHITE)
        msg_rect = msg_surface.get_rect(center=(self.screen.get_width() // 2, dialog_y + 60))
        self.screen.blit(msg_surface, msg_rect)

        # Opções (destacando a selecionada)
        yes_color = COLOR_GREEN if self.confirmation_selection == 1 else COLOR_WHITE
        no_color = COLOR_GREEN if self.confirmation_selection == 0 else COLOR_WHITE

        yes_surface = FONT_OPTION.render('YES', True, yes_color)
        no_surface = FONT_OPTION.render('NO', True, no_color)

        yes_rect = yes_surface.get_rect(center=(self.screen.get_width() // 2 - 80, dialog_y + 130))
        no_rect = no_surface.get_rect(center=(self.screen.get_width() // 2 + 80, dialog_y + 130))

        self.screen.blit(yes_surface, yes_rect)
        self.screen.blit(no_surface, no_rect)

        # Instruções
        instructions = FONT_OPTION.render('Use LEFT/RIGHT to choose, ENTER to confirm', True, COLOR_GREEN)
        instructions_rect = instructions.get_rect(center=(self.screen.get_width() // 2, dialog_y + 170))
        self.screen.blit(instructions, instructions_rect)

    def run(self):
        menu_option = 0
        clock = pygame.time.Clock()

        # Inicia o som do menu
        self.start_menu_sound()

        while True:
            # Se não estiver em confirmação, desenha o menu normal
            if not self.in_confirmation:
                self.screen.fill(COLOR_BLACK)

                title_surface = FONT_TITLE_MENU.render('蛇ちゃんゲーム', True, COLOR_WHITE)
                title_rect = title_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4))
                self.screen.blit(title_surface, title_rect)

                for i in range(len(MENU_OPTION)):
                    if i == menu_option:
                        self.menu_text(40, MENU_OPTION[i], COLOR_GREEN, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + i * 60))
                    else:
                        self.menu_text(40, MENU_OPTION[i], COLOR_WHITE, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + i * 60))

            # Se estiver em confirmação, desenha o diálogo
            else:
                self.draw_confirmation_dialog("Quit Game?")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Se estiver em modo de confirmação
                    if self.in_confirmation:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.confirmation_selection = 1 - self.confirmation_selection
                            self.option_sound.play()

                        elif event.key == pygame.K_RETURN:
                            self.select_sound.play()
                            if self.confirmation_selection == 1:  # YES
                                if self.confirmation_target == "exit":
                                    pygame.quit()
                                    sys.exit()
                            else:  # NO
                                self.in_confirmation = False
                                self.confirmation_target = None

                    # Se não estiver em confirmação (menu normal)
                    else:
                        if event.key == pygame.K_DOWN:  # DOWN KEY
                            if menu_option < len(MENU_OPTION) - 1:
                                menu_option += 1
                            else:
                                menu_option = 0
                            self.option_sound.play()

                        if event.key == pygame.K_UP:  # UP KEY
                            if menu_option > 0:
                                menu_option -= 1
                            else:
                                menu_option = len(MENU_OPTION) - 1
                            self.option_sound.play()

                        if event.key == pygame.K_RETURN:  # ENTER KEY
                            self.select_sound.play()

                            if menu_option == 0:  # Play
                                self.menu_sound.stop()
                                game = Game()
                                # Executa o jogo e verifica se precisa voltar ao menu
                                return_to_menu = game.run()

                                # Se o jogo retornou ao menu, reinicia o som
                                if return_to_menu or return_to_menu is None:
                                    self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                                    self.start_menu_sound()

                            elif menu_option == 1:  # score
                                self.show_scores()
                                # Para temporariamente o som do menu
                                self.menu_sound.stop()
                                while True:
                                    for events in pygame.event.get():
                                        if events.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if events.type == pygame.KEYDOWN:
                                            if events.key == pygame.K_RETURN:
                                                self.screen.fill(COLOR_BLACK)
                                                # Reinicia o som do menu
                                                self.start_menu_sound()
                                                break
                                    else:
                                        continue
                                    break

                            elif menu_option == 2:  # Exit
                                # Em vez de sair direto, mostra confirmação
                                self.in_confirmation = True
                                self.confirmation_selection = 0
                                self.confirmation_target = "exit"

            clock.tick(FPS)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)