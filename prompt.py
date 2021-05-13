"""
File: prompt.py

This file contains the prompt class that contains the data for each character in the prompt.
"""
from letter import Letter


class Prompt:
    def __init__(self, text):
        self.text = text
        self.char_list = self.create_char_list()

    def create_char_list(self):
        char_list = []
        for ch in self.text:
            char_list.append(Letter(ch))
        return char_list
