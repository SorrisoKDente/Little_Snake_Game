import pygame, sys

from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_BLACK, FONT_TITLE_MENU, COLOR_WHITE, COLOR_GREEN, FONT_OPTION, FPS, \
    MENU_OPTION
from code.Game import Game

pygame.init()


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('蛇ちゃんゲーム Game Menu')

    def run(self):
        menu_option = 0
        clock = pygame.time.Clock()
        while True:
            title_surface = FONT_TITLE_MENU.render('蛇ちゃんゲーム', True, COLOR_WHITE)
            title_rect = title_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4))
            self.screen.blit(title_surface, title_rect)

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(40, MENU_OPTION[i], COLOR_GREEN, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + i * 60))
                else:
                    self.menu_text(40, MENU_OPTION[i], COLOR_WHITE, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + i * 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # end pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: #DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP: #UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN: #ENTER KEY
                        if menu_option == 0: #Play
                            game = Game()
                            game.run()
                        else:  # Exit
                            pygame.quit()
                            sys.exit()

            clock.tick(FPS)


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)
