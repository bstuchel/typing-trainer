"""
File: game.py

This file contains the typing game logic.
"""
import json
import random
import time


class Game:
    PROMPT_LENGTH = 15 

    def __init__(self):
        self.__lexicon = self.__get_lexicon()
        self.chosen_words = self.choose_words()
        # Prompt data
        self.prompt_text = self.get_prompt()
        self.prompt_size = self.PROMPT_LENGTH
        # Timing data
        self.start_time = 0
        self.stop_time = 1

    @staticmethod
    def __get_lexicon():
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def choose_words(self):
        chosen_words = []
        while len(chosen_words) < self.PROMPT_LENGTH:
            choice = random.choice(self.__lexicon)
            if len(chosen_words) == 0 or choice != chosen_words[-1]:  # Avoid back to back words
                chosen_words.append(choice)
        return chosen_words

    def clear_words(self):
        self.chosen_words.clear()

    def get_prompt(self):
        prompt = ""
        for word in self.chosen_words:
            prompt += word + ' '
        return prompt[:-1]

    def start_clock(self):
        self.start_time = time.time()

    def stop_clock(self):
        self.stop_time = time.time()

    def get_runtime(self):
        return self.stop_time - self.start_time
