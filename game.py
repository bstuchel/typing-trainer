"""
File: game.py

This file contains the typing game logic.
"""
import json
import random

class Game:
    PROMPT_LENGTH = 45  # Words in prompt
    GAME_LENGTH = 30    # Time in seconds

    def __init__(self):
        # Prompt data
        self.__lexicon = self.__get_lexicon()
        self.chosen_words = []
        self.prompt_text = ""
        self.prompt_size = self.PROMPT_LENGTH
        # Timing data
        self.time_remaining = self.GAME_LENGTH
        self.words_typed = 0
        self.score = 0
        self.new_game()


    @staticmethod
    def __get_lexicon():
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def new_game(self):
        self.chosen_words = self.choose_words()
        self.prompt_text = self.get_prompt()
        self.time_remaining = self.GAME_LENGTH
        self.words_typed = 0
        self.score = 0

    def choose_words(self):
        chosen_words = []
        while len(chosen_words) < self.PROMPT_LENGTH:
            choice = random.choice(self.__lexicon)
            if len(chosen_words) == 0 or choice != chosen_words[-1]:  # Avoid back to back words
                chosen_words.append(choice)
        return chosen_words

    def get_prompt(self):
        prompt = ""
        for word in self.chosen_words:
            prompt += word + ' '
        return prompt[:-1]

    def tick_timer(self):
        self.time_remaining -= 1

    def end_game(self, typed):
        correct_words = self.get_correct_words(typed)
        self.score = 60 * correct_words // self.GAME_LENGTH

    def get_correct_words(self, typed):
        correct_words = 0
        i = 0
        while i < len(typed):
            while i < len(typed) and typed[i] == self.prompt_text[i]:
                if typed[i] == ' ':
                   correct_words += 1
                   break
                i += 1
            while i < len(typed) and typed[i] != ' ':
                i += 1
            i += 1
        return correct_words
