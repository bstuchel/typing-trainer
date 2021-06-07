"""
File: game.py

This file contains the typing game logic.
"""
import json
import random
from word import Word

class Game:
    PROMPT_LENGTH = 45  # Words in prompt
    GAME_LENGTH = 30    # Time in seconds

    def __init__(self):
        # Prompt data
        self.__lexicon = self.__get_lexicon()
        self.words = []
        self.prompt_size = self.PROMPT_LENGTH
        self.word_idx = 0
        self.letter_idx = 0
        # Timing data
        self.time_remaining = self.GAME_LENGTH
        self.score = 0
        self.new_game()

    @staticmethod
    def __get_lexicon():
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def new_game(self):
        self.choose_words()
        self.time_remaining = self.GAME_LENGTH
        self.score = 0
        self.word_idx = 0
        self.letter_idx = 0

    def choose_words(self):
        last = ""
        while len(self.words) < self.PROMPT_LENGTH:
            choice = random.choice(self.__lexicon)
            if choice != last:  # Avoid back to back words
                last = choice
                self.words.append(Word(choice))

    def next_char(self):
        self.letter_idx += 1
        if self.letter_idx == len(self.words[self.word_idx].char_list):
            self.word_idx += 1
            self.letter_idx = 0

    def prev_char(self):
        if self.word_idx != 0 or self.letter_idx != 0:
            self.letter_idx -= 1
            if self.letter_idx == -1:
                self.word_idx -= 1
                self.letter_idx = len(self.words[self.word_idx].char_list) - 1

    def get_char(self):
        return self.words[self.word_idx].char_list[self.letter_idx]

    def tick_timer(self):
        self.time_remaining -= 1

    def end_game(self, typed):
        correct_words = self.get_correct_words(typed)
        self.score = 60 * correct_words // self.GAME_LENGTH

    def get_correct_words(self, typed):
        return 1
        ### This needs to be reworked
        # correct_words = 0
        # i = 0
        # while i < len(typed):
        #     while i < len(typed) and typed[i] == self.prompt_text[i]:
        #         if typed[i] == ' ':
        #            correct_words += 1
        #            break
        #         i += 1
        #     while i < len(typed) and typed[i] != ' ':
        #         i += 1
        #     i += 1
        # return correct_words
