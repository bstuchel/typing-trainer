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
        """ Create display surfaces """
        self.dis = self.create_display()
        self.prompt_surf = pygame.Surface((self.PROMPT_SURF_WIDTH, 
                                           self.PROMPT_SURF_HEIGHT))
        self.timer_surf = pygame.Surface((self.TIMER_SURF_WIDTH, 
                                          self.TIMER_SURF_HEIGHT))

    def set_game(self, game):
        """ Set the gui for a give game object
        :param game.Game game: Game object
        """
        self.game = game
        self.update_timer()
        self.update_prompt()

    def create_display(self):
        """ Create the display surface using the defined parameters """
        dis = pygame.display.set_mode((self.DIS_WIDTH, self.DIS_HEIGHT))
        pygame.display.set_caption("Typing Practice")
        dis.fill(self.BLUE_BACKGROUND)
        return dis

    def update_display(self):
        """ Update the timer and prompt to the screen """
        self.dis.fill(self.BLUE_BACKGROUND)
        self.update_timer()
        self.update_prompt()
        pygame.display.update()

    def update_timer(self):
        """ Update the timer based on the Game object """
        self.timer_surf.fill(self.BLUE_BACKGROUND)
        self.LARGE_FONT.render_to(self.timer_surf, 
                                  (0, 0), 
                                  str(self.game.time_remaining), 
                                  self.DARK_BLUE_TEXT)
        self.dis.blit(self.timer_surf, (self.TIMER_X, self.TIMER_Y))

    def update_prompt(self):
        """ Update the prompt by iterating over each letter of typed and 
        untyped characters 
        """
        self.prompt_surf.fill(self.BLUE_BACKGROUND)
        i = 0
        x = 0
        y = self.SMALL_FONT_SIZE
        while i < len(self.game.display_prompt):
            word = self.game.display_prompt[i]
            x, y = self.get_pos(x, y, word.width)
            j = 0
            while j < len(word.char_list):
                self.SMALL_FONT.render_to(self.prompt_surf, (x, y), 
                                          word.char_list[j].ch, 
                                          word.char_list[j].color)
                self.draw_cursor(i, j, x, y)
                x += word.char_list[j].width
                j += 1
            self.draw_cursor(i, j, x, y)
            self.SMALL_FONT.render_to(self.prompt_surf, (x, y), 
                                      ' ', self.WHITE)
            x += self.SMALL_SPACE_WIDTH
            i += 1

        self.dis.blit(self.prompt_surf, (self.PROMPT_X, self.PROMPT_Y))

    def get_pos(self, x, y, width):
        """ If the give width will not fit on the current line, the text must 
        be wrapped to the next line by updating x and y. 
        :param int x: Current horizontal location on display
        :param int y: Current vertical location on display
        :param int width: Width of the word to be drawn
        :return: The updated x and y locations
        :rtype: tuple(int, int)
        """
        if x + width > self.PROMPT_SURF_WIDTH:
            y += self.SMALL_FONT_SIZE * 3 // 2
            x = 0
        return x, y

    def draw_cursor(self, i, j, x, y):
        """ A cursor will be drawin if the cursor location 
        :param int i: The current word being drawn
        :param int j: The current letter in the word being drawn
        :param int x: Current horizontal location on display
        :param int y: Current vertical location on display 
        """
        if i == self.game.word_idx and j == self.game.letter_idx:
            cursor = pygame.Rect(x, y - self.SMALL_FONT_SIZE, 2, self.SMALL_FONT_SIZE * 4 // 3)
            pygame.draw.rect(self.prompt_surf, self.WHITE, cursor)

    def display_score(self):
        """ Create and display the score screen to the display """
        self.dis.fill(self.BLUE_BACKGROUND)

        # Create score surface
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

        # Blit to display
        x = (self.DIS_WIDTH - width) // 2
        y = self.DIS_HEIGHT * 2 // 3 - height // 2
        self.dis.blit(play_again_surf, (x, y))

        pygame.display.update()

    def write_line(self, text, font, surf, y):
        """ Write text to a surface using the given font.  Center the text 
        on the surface and place at the given y value 
        :param str text: The text to be drawn on the surface
        :param pygame.freetype.Font font: The font to be used
        :param pygame.Surface surf: The surface to be drawn on
        :param int y: The vertical location to be drawn at
        """
        text_rect = font.get_rect(text)
        text_width = text_rect.width
        width = surf.get_size()[0]
        x = (width - text_width) // 2
        font.render_to(surf, (x, y), text, self.WHITE)
