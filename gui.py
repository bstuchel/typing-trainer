"""
File: gui.py

This file contains the gui class for the typing application.
"""
import pygame
import pygame.freetype
pygame.init()


class Gui:
    # Define colors
    BLUE_BACKGROUND = (36, 41, 51)
    DARK_BLUE_TEXT = (27, 31, 38)
    WHITE = (214, 220, 231)

    # Define fonts
    FONT_PATHNAME = "res/fonts/RobotoMono-Medium.ttf"

    SMALL_FONT_SIZE = 30
    SMALL_FONT = pygame.freetype.Font(FONT_PATHNAME, SMALL_FONT_SIZE)
    SMALL_FONT.origin = True
    SMALL_SPACE_WIDTH = SMALL_FONT.get_metrics(' ')[0][4]

    LARGE_FONT_SIZE = 100
    LARGE_FONT = pygame.freetype.Font(FONT_PATHNAME, LARGE_FONT_SIZE)
    LARGE_FONT.origin = False
    
    # Define surface geometry
    DIS_WIDTH = 1080
    DIS_HEIGHT = 720

    PROMPT_SURF_WIDTH = DIS_WIDTH * 2 // 3
    PROMPT_SURF_HEIGHT = DIS_HEIGHT // 2
    PROMPT_X = (DIS_WIDTH - PROMPT_SURF_WIDTH) // 2
    PROMPT_Y = (DIS_HEIGHT - PROMPT_SURF_HEIGHT) // 2

    TIMER_SURF_WIDTH = LARGE_FONT_SIZE * 2
    TIMER_SURF_HEIGHT = LARGE_FONT_SIZE
    TIMER_X = (DIS_WIDTH - TIMER_SURF_WIDTH) // 2
    TIMER_Y = (PROMPT_X - TIMER_SURF_HEIGHT) // 2

    def __init__(self):
        # Display surfaces
        self.dis = self.create_display()
        self.prompt_surf = pygame.Surface((self.PROMPT_SURF_WIDTH, self.PROMPT_SURF_HEIGHT))
        self.timer_surf = pygame.Surface((self.TIMER_SURF_WIDTH, self.TIMER_SURF_HEIGHT))

    def set_game(self, game):
        self.game = game
        self.update_timer()
        self.update_prompt()

    def create_display(self):
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def update_prompt(self):
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        x = 0
        y = self.SMALL_FONT_SIZE
        for word in self.game.words:
            if x + word.width > self.PROMPT_SURF_WIDTH:
                y += self.SMALL_FONT_SIZE * 3 // 2
                x = 0
            for letter in word.char_list:
                self.SMALL_FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
                x += letter.width
            self.SMALL_FONT.render_to(self.prompt_surf, (x, y), ' ', self.WHITE)
            x += self.SMALL_SPACE_WIDTH
        self.dis.blit(self.prompt_surf, (self.PROMPT_X, self.PROMPT_Y))
        pygame.display.update()

    def update_timer(self):
        self.timer_surf.fill(self.BLUE_BACKGROUND)
        self.LARGE_FONT.render_to(self.timer_surf, (0, 0), str(self.game.time_remaining), self.DARK_BLUE_TEXT)
        self.dis.blit(self.timer_surf, (self.TIMER_X, self.TIMER_Y))
        pygame.display.update()

    def display_score(self):
        self.dis.fill(self.BLUE_BACKGROUND)
        # Display score
        result_surf = self.LARGE_FONT.render(f"WPM: {self.game.score}", self.WHITE, self.BLUE_BACKGROUND)[0]
        width, height = result_surf.get_size()
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT // 3 - height // 2
        self.dis.blit(result_surf, (x, y))
        # Display play again instructions
        play_again_surf = self.SMALL_FONT.render("Press enter to play again", self.WHITE, self.BLUE_BACKGROUND)[0]
        width, height = play_again_surf.get_size()
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT * 2 // 3 - height // 2
        self.dis.blit(play_again_surf, (x, y))
        pygame.display.update()
