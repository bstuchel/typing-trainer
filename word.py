"""
File: word.py

This file contains the word class which are used to make up the prompt.
"""
from letter import Letter

class Word:
    def __init__(self, text):
        self.char_list = [] 
        self.create_word(text)

    def create_word(self, text):
        for ch in text:
            self.char_list.append(Letter(ch))
