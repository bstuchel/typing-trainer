"""
File: game.py

This file contains the typing game logic.
"""
import json
import random
import time


class Game:
    def __init__(self):
        self.__lexicon = self.__get_lexicon()
        self.chosen_words = self.choose_words()
        self.start_time = 0
        self.stop_time = 1

    @staticmethod
    def __get_lexicon():
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def choose_words(self):
        chosen_words = []
        while len(chosen_words) < 7:
            choice = random.choice(self.__lexicon)
            if len(chosen_words) == 0 or choice != chosen_words[-1]:  # No back to back words
                chosen_words.append(choice)
        return chosen_words

    def clear_words(self):
        self.chosen_words.clear()

    def get_prompt(self):
        prompt = ""
        line_length = 0
        for word in self.chosen_words:
            if line_length + len(word) + 1 > 50:
                prompt += "\n"
                line_length = 0
            prompt += word + ' '
            line_length += len(word) + 1
        return prompt[:-1]

    def start_clock(self):
        self.start_time = time.time()

    def stop_clock(self):
        self.stop_time = time.time()

    def get_runtime(self):
        return self.stop_time - self.start_time
