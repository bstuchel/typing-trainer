"""
File: gui.py

This file contains the gui class for the typing application.
"""
from prompt import Prompt
import pygame
import pygame.freetype
pygame.init()


class Gui:
    DIS_WIDTH = 1080
    DIS_HEIGHT = 720

    # Define colors
    BLUE_BACKGROUND = (36, 41, 51)
    DARK_BLUE_TEXT = (27, 31, 38)
    CURSOR = (214, 220, 231)            # White

    # Define fonts
    FONT_PATHNAME = "res/fonts/RobotoMono-Medium.ttf"
    FONT = pygame.freetype.Font(FONT_PATHNAME, 30)
    FONT.origin = True

    def __init__(self, text):
        self.dis = self.create_display()
        self.prompt_surf = self.create_prompt_surf()
        self.prompt = Prompt(text)
        self.metrics = self.FONT.get_metrics(text)
        self.prompt_surf_rect = self.FONT.get_rect(text)
        self.baseline = self.prompt_surf_rect.y
        self.prompt_surf_rect.center = self.dis.get_rect().center

    def create_display(self):
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def create_prompt_surf(self):
        prompt_surface = pygame.Surface((self.DIS_WIDTH // 2, self.DIS_HEIGHT // 4))
        return prompt_surface

    def update_display(self):
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        x = 0
        # render each letter of the current sentence one by one
        for letter, metric in zip(self.prompt.char_list, self.metrics):
            # render the single letter
            self.FONT.render_to(self.prompt_surf, (x, self.baseline), letter.ch, letter.color)
            # and move the start position
            x += metric[4]
        self.dis.blit(self.prompt_surf, (self.DIS_WIDTH // 4, 3 * self.DIS_HEIGHT // 8))
        pygame.display.update()
