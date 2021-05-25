"""
File: gui.py

This file contains the gui class for the typing application.
"""
from letter import Letter
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
    CURSOR = (214, 220, 231)

    # Define fonts
    FONT_PATHNAME = "res/fonts/RobotoMono-Medium.ttf"
    FONT_SIZE = 30
    FONT = pygame.freetype.Font(FONT_PATHNAME, FONT_SIZE)
    FONT.origin = True

    def __init__(self, game):
        # Display surfaces
        self.dis = self.create_display()
        self.prompt_surf = self.create_prompt_surf()
        # Prompt information
        self.prompt_text = game.prompt_text
        self.prompt_surf_rect = self.FONT.get_rect(game.prompt_text)
        self.baseline = self.prompt_surf_rect.y
        self.char_list = self.get_char_list()
        self.set_display()

    def create_display(self):
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def create_prompt_surf(self):
        prompt_surface = pygame.Surface((self.PROMPT_SURF_WIDTH, self.PROMPT_SURF_HEIGHT))
        return prompt_surface

    def get_char_list(self):
        char_list = []
        x = 0
        y = self.baseline
        for ch in self.prompt_text:
            char_list.append(Letter(ch, x, y))
            x += self.FONT.get_metrics(ch)[0][4]
            if (x >= self.PROMPT_SURF_WIDTH * 3 // 4 and ch == ' '):
                x = 0
                y += self.FONT_SIZE * 4 // 3
        return char_list                

    def set_display(self):
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        for letter in self.char_list:
            self.FONT.render_to(self.prompt_surf, letter.location, letter.ch, letter.color)
        self.dis.blit(self.prompt_surf, ((self.DIS_WIDTH//2) - (self.PROMPT_SURF_WIDTH//2), (self.DIS_HEIGHT//2) - (self.PROMPT_SURF_HEIGHT//2)))
        pygame.display.update()

    def update_display(self, index):
        if index != -1:
            letter = self.char_list[index]
            rect = pygame.Rect(letter.location[0], letter.location[1] - self.baseline, self.FONT.get_metrics(letter.ch)[0][4], self.FONT_SIZE * 4 // 3)
            pygame.draw.rect(self.prompt_surf, self.BLUE_BACKGROUND, rect)
            self.FONT.render_to(self.prompt_surf, letter.location, letter.ch, letter.color)
            self.dis.blit(self.prompt_surf, ((self.DIS_WIDTH//2) - (self.PROMPT_SURF_WIDTH//2), (self.DIS_HEIGHT//2) - (self.PROMPT_SURF_HEIGHT//2)))
            pygame.display.update()
