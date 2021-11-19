"""
File: word.py

This file contains the word class which are used to make up the prompt.
"""
from letter import Letter

class Word:
    def __init__(self, text=""):
        self.char_list = [] 
        self.width = 0
        self.create_word(text)
        self.is_correct = True

    def create_word(self, text):
        """ Create a word by creating a list of Letter objects 
        :param str text: The word as a string
        """
        for ch in text:
            self.char_list.append(Letter(ch))
            self.width += self.char_list[-1].width

    def add_text(self, ch):
        """ Add text to the word's char_list and adjust the word width 
        :param str ch: The character to be added
        """
        self.char_list.append(Letter(ch))
        self.width += self.char_list[-1].width

    def add_letter(self, letter):
        """ Add a given Letter object to the word and adjust the word width
        :param letter.Letter letter: The letter object to be added
        """
        self.char_list.append(letter)
        self.width += self.char_list[-1].width

    def remove_last(self):
        """ Remove the last character from a word and adjust the width """
        self.width -= self.char_list.pop().width
        