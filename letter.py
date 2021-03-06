"""
File: letter.py

This file contains the letter class used to make up the prompt in the typing application.
"""
from gui import Gui

class Letter:
    # Text colors
    DEFAULT = (93, 109, 124)        # Light blue
    CORRECT = (214, 220, 231)       # White
    INCORRECT = (190, 97, 106)      # Red

    def __init__(self, ch):
        self.ch = ch
        self.color = self.DEFAULT
        self.width = Gui.SMALL_FONT.get_metrics(ch)[0][4] # Width of letter based on the font from the Gui class

    def set_correct(self):
        """ Set the letter color for a correct input """
        self.color = self.CORRECT

    def set_incorrect(self):
        """ Set the letter color for an incorrect input """
        self.color = self.INCORRECT

    def set_default(self):
        """ Set the letter color to be the default """
        self.color = self.DEFAULT
