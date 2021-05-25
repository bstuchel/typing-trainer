"""
File: game.py

This file contains the typing game logic.
"""
import json
import random

class Game:
    PROMPT_LENGTH = 15 

    def __init__(self):
        self.__lexicon = self.__get_lexicon()
        self.chosen_words = self.choose_words()
        # Prompt data
        self.prompt_text = self.get_prompt()
        self.prompt_size = self.PROMPT_LENGTH
        # Timing data
        self.time_remaining = 30
        self.words_typed = 0

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

    def tick_timer(self):
        self.time_remaining -= 1

    def end_game(self, typed):
       pass

    def get_runtime(self):
        return self.stop_time - self.start_time
