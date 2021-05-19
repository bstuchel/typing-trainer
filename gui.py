"""
File: gui.py

This file contains the gui class for the typing application.
"""
import pygame
import pygame.freetype
pygame.init()


class Gui:
    DIS_WIDTH = 1080
    DIS_HEIGHT = 720

    PROMPT_SURF_WIDTH = DIS_WIDTH * 2 // 3
    PROMPT_SURF_HEIGHT = DIS_HEIGHT // 4

    # Define colors
    BLUE_BACKGROUND = (36, 41, 51)
    DARK_BLUE_TEXT = (27, 31, 38)
    CURSOR = (214, 220, 231)            # White

    # Define fonts
    FONT_PATHNAME = "res/fonts/RobotoMono-Medium.ttf"
    FONT_SIZE = 30
    FONT = pygame.freetype.Font(FONT_PATHNAME, FONT_SIZE)
    FONT.origin = True

    def __init__(self, game):
        self.dis = self.create_display()
        self.prompt_surf = self.create_prompt_surf()
        self.prompt_text = game.prompt_text
        self.prompt_char_list = game.prompt_char_list
        self.metrics = self.FONT.get_metrics(game.prompt_text)
        self.prompt_surf_rect = self.FONT.get_rect(game.prompt_text)
        self.baseline = self.prompt_surf_rect.y

    def create_display(self):
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def create_prompt_surf(self):
        prompt_surface = pygame.Surface((self.PROMPT_SURF_WIDTH, self.PROMPT_SURF_HEIGHT))
        return prompt_surface

    def update_display(self):
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        x = 0
        y = self.baseline
        # render each letter of the current sentence one by one
        for letter, metric in zip(self.prompt_char_list, self.metrics):
            if x >= self.PROMPT_SURF_WIDTH * 3 // 4 and letter.ch == ' ':
                self.FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
                x = 0
                y += self.FONT_SIZE * 4 // 3    # Go to new line with margin of 1/3 text height
                continue
            # render the single letter
            self.FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
            # and move the start position
            x += metric[4]
        self.dis.blit(self.prompt_surf, ((self.DIS_WIDTH//2) - (self.PROMPT_SURF_WIDTH//2), (self.DIS_HEIGHT//2) - (self.PROMPT_SURF_HEIGHT//2)))
        pygame.display.update()
