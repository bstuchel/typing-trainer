"""
File: gui.py

This file contains the gui class for the typing application.
"""
from letter import Letter
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

    PROMPT_FONT_SIZE = 30
    PROMPT_FONT = pygame.freetype.Font(FONT_PATHNAME, PROMPT_FONT_SIZE)
    PROMPT_FONT.origin = True

    TIMER_FONT_SIZE = 100
    TIMER_FONT = pygame.freetype.Font(FONT_PATHNAME, TIMER_FONT_SIZE)
    TIMER_FONT.origin = False
    
    DIS_WIDTH = 1080
    DIS_HEIGHT = 720

    PROMPT_SURF_WIDTH = DIS_WIDTH * 2 // 3
    PROMPT_SURF_HEIGHT = DIS_HEIGHT // 2
    PROMPT_X = (DIS_WIDTH//2) - (PROMPT_SURF_WIDTH//2)
    PROMPT_Y = (DIS_HEIGHT//2) - (PROMPT_SURF_HEIGHT//2)

    TIMER_SURF_WIDTH = TIMER_FONT_SIZE * 2
    TIMER_SURF_HEIGHT = TIMER_FONT_SIZE
    TIMER_X = (DIS_WIDTH//2) - (TIMER_SURF_WIDTH//2)
    TIMER_Y = (PROMPT_X//2) - (TIMER_SURF_HEIGHT//2)

    def __init__(self):
        # Display surfaces
        self.dis = self.create_display()
        self.prompt_surf = pygame.Surface((self.PROMPT_SURF_WIDTH, self.PROMPT_SURF_HEIGHT))
        self.timer_surf = pygame.Surface((self.TIMER_SURF_WIDTH, self.TIMER_SURF_HEIGHT))

    def set_game(self, game):
        self.game = game
        self.prompt_text = game.prompt_text
        self.prompt_surf_rect = self.PROMPT_FONT.get_rect(game.prompt_text)
        self.prompt_baseline = self.prompt_surf_rect.y
        self.char_list = self.get_char_list()
        self.set_display()

    def create_display(self):
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def get_char_list(self):
        char_list = []
        x = 0
        y = self.prompt_baseline
        for ch in self.prompt_text:
            char_list.append(Letter(ch, x, y))
            x += self.PROMPT_FONT.get_metrics(ch)[0][4]
            if (x >= self.PROMPT_SURF_WIDTH * 3 // 4 and ch == ' '):
                x = 0
                y += self.PROMPT_FONT_SIZE * 4 // 3
        return char_list                

    def set_display(self):
        self.timer_surf.fill(self.BLUE_BACKGROUND)
        self.TIMER_FONT.render_to(self.timer_surf, (0, 0), str(self.game.time_remaining), self.DARK_BLUE_TEXT)
        self.dis.blit(self.timer_surf, (self.TIMER_X, self.TIMER_Y))

        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        for letter in self.char_list:
            self.PROMPT_FONT.render_to(self.prompt_surf, letter.location, letter.ch, letter.color)
        self.dis.blit(self.prompt_surf, (self.PROMPT_X, self.PROMPT_Y))
        pygame.display.update()

    def update_prompt(self, index):
        if index != -1:
            letter = self.char_list[index]
            rect = pygame.Rect(letter.location[0], letter.location[1] - self.prompt_baseline, self.PROMPT_FONT.get_metrics(letter.ch)[0][4], self.PROMPT_FONT_SIZE * 4 // 3)
            pygame.draw.rect(self.prompt_surf, self.BLUE_BACKGROUND, rect)
            self.PROMPT_FONT.render_to(self.prompt_surf, letter.location, letter.ch, letter.color)
            self.dis.blit(self.prompt_surf, ((self.DIS_WIDTH//2) - (self.PROMPT_SURF_WIDTH//2), (self.DIS_HEIGHT//2) - (self.PROMPT_SURF_HEIGHT//2)))
            pygame.display.update()

    def update_timer(self):
        self.timer_surf.fill(self.BLUE_BACKGROUND)
        self.TIMER_FONT.render_to(self.timer_surf, (0, 0), str(self.game.time_remaining), self.DARK_BLUE_TEXT)
        self.dis.blit(self.timer_surf, (self.TIMER_X, self.TIMER_Y))
        pygame.display.update()

    def display_score(self, score):
        self.dis.fill(self.BLUE_BACKGROUND)
        # Display score
        result_surf = self.TIMER_FONT.render(f"WPM: {score}", self.WHITE, self.BLUE_BACKGROUND)[0]
        width, height = result_surf.get_size()
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT // 3 - height // 2
        self.dis.blit(result_surf, (x, y))
        # Display play again instructions
        play_again_surf = self.PROMPT_FONT.render("Press enter to play again", self.WHITE, self.BLUE_BACKGROUND)[0]
        width, height = play_again_surf.get_size()
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT * 2 // 3 - height // 2
        self.dis.blit(play_again_surf, (x, y))
        pygame.display.update()
