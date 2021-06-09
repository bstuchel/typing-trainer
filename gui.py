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

    MED_FONT_SIZE = 50
    MED_FONT = pygame.freetype.Font(FONT_PATHNAME, MED_FONT_SIZE)
    MED_FONT.origin = True

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

    def update_display(self):
        self.dis.fill(self.BLUE_BACKGROUND)
        self.update_timer()
        self.update_prompt()
        pygame.display.update()

    def update_timer(self):
        self.timer_surf.fill(self.BLUE_BACKGROUND)
        self.LARGE_FONT.render_to(self.timer_surf, (0, 0), str(self.game.time_remaining), self.DARK_BLUE_TEXT)
        self.dis.blit(self.timer_surf, (self.TIMER_X, self.TIMER_Y))

    def update_prompt(self):
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        i = 0
        x = 0
        y = self.SMALL_FONT_SIZE

        # Print completed words
        while i < self.game.word_idx:
            input_word = self.game.input[i]
            x, y = self.check_text_wrap(x, y, input_word.width)
            j = 0
            while j < len(input_word.char_list):
                letter = input_word.char_list[j]
                self.SMALL_FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
                x += letter.width
                j += 1
            while j < len(self.game.prompt[i].char_list):
                # The word wasn't completed
                letter = self.game.prompt[i].char_list[j]
                self.SMALL_FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
                x += letter.width
                j += 1
            self.SMALL_FONT.render_to(self.prompt_surf, (x, y), ' ', self.WHITE)
            x += self.SMALL_SPACE_WIDTH
            i += 1

        # Print current word and cursor
        input_word = self.game.input[i]
        word = self.game.prompt[i]
        if len(input_word.char_list) > len(word.char_list):
            word = input_word
        x, y = self.check_text_wrap(x, y, word.width)
        j = 0
        while j < len(word.char_list):
            if j == self.game.letter_idx:  
                # Print cursor
                pygame.draw.rect(self.prompt_surf, self.WHITE, pygame.Rect(x, y - self.SMALL_FONT_SIZE, 2, self.SMALL_FONT_SIZE * 4 // 3))
            letter = word.char_list[j]
            self.SMALL_FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
            x += letter.width
            j += 1
        if j == self.game.letter_idx:
            # Print cursor
            pygame.draw.rect(self.prompt_surf, self.WHITE, pygame.Rect(x, y - self.SMALL_FONT_SIZE, 2, self.SMALL_FONT_SIZE * 4 // 3))
        self.SMALL_FONT.render_to(self.prompt_surf, (x, y), ' ', self.WHITE)
        x += self.SMALL_SPACE_WIDTH
        i += 1      

        # Print remaining prompt
        while i < len(self.game.prompt):
            word = self.game.prompt[i]
            x, y = self.check_text_wrap(x, y, word.width)
            for letter in word.char_list:
                self.SMALL_FONT.render_to(self.prompt_surf, (x, y), letter.ch, letter.color)
                x += letter.width
            self.SMALL_FONT.render_to(self.prompt_surf, (x, y), ' ', self.WHITE)
            x += self.SMALL_SPACE_WIDTH
            i += 1

        # Display prompt surface
        self.dis.blit(self.prompt_surf, (self.PROMPT_X, self.PROMPT_Y))

    def check_text_wrap(self, x, y, width):
        if x + width > self.PROMPT_SURF_WIDTH:
            y += self.SMALL_FONT_SIZE * 3 // 2
            x = 0
        return x, y

    def display_score(self):
        self.dis.fill(self.BLUE_BACKGROUND)
        height = self.SMALL_FONT_SIZE * 4 + self.MED_FONT_SIZE
        width = self.DIS_WIDTH
        score_surf = pygame.Surface((width, height))
        score_surf.fill(self.BLUE_BACKGROUND)
        # Display raw score
        text = f"Raw WPM: {self.game.raw_score}"
        y = self.SMALL_FONT_SIZE
        self.write_line(text, self.SMALL_FONT, score_surf, y)
        # Display incorrect words
        text = f"Incorrect Words: {self.game.incorrect_words}"
        y = self.SMALL_FONT_SIZE*3
        self.write_line(text, self.SMALL_FONT, score_surf, y)
        # Display adjusted score
        text = f"Adjusted WPM: {self.game.score}"
        y = self.SMALL_FONT_SIZE * 4 + self.MED_FONT_SIZE
        self.write_line(text, self.MED_FONT, score_surf, y)
        # Blit to display
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT // 3 - height // 2
        self.dis.blit(score_surf, (x, y))
        # Display play again instructions
        play_again_surf = self.SMALL_FONT.render("Press enter to play again", self.WHITE, self.BLUE_BACKGROUND)[0]
        width, height = play_again_surf.get_size()
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT * 2 // 3 - height // 2
        self.dis.blit(play_again_surf, (x, y))
        pygame.display.update()

    def write_line(self, text, font, surf, y):
        text_rect = font.get_rect(text)
        text_width = text_rect.width
        width = surf.get_size()[0]
        x = (width - text_width) // 2
        font.render_to(surf, (x, y), text, self.WHITE)