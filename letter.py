"""
File: letter.py

This file contains the letter class used to make up the prompt in the typing application.
"""

class Letter:
    # Text colors
    DEFAULT = (93, 109, 124)        # Light blue
    CORRECT = (214, 220, 231)       # White
    INCORRECT = (190, 97, 106)      # Red

    def __init__(self, ch, x, y):
        self.ch = ch
        self.color = self.DEFAULT
        self.location = (x, y)        

    def set_correct(self):
        self.color = self.CORRECT

    def set_incorrect(self):
        self.color = self.INCORRECT

    def set_default(self):
        self.color = self.DEFAULT
