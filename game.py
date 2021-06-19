"""
File: game.py

This file contains the typing game logic.
"""
import json
import random
from word import Word

class Game:
    PROMPT_LENGTH = 50  # Words in prompt
    GAME_LENGTH = 30    # Time in seconds

    def __init__(self):
        # Prompt data
        self.__lexicon = self.__get_lexicon()
        self.prompt = []
        self.prompt_size = self.PROMPT_LENGTH
        # User input data
        self.input = []
        self.word_idx = 0
        self.letter_idx = 0
        # Timing data
        self.time_remaining = self.GAME_LENGTH
        self.raw_score = 0        
        self.incorrect_words = 0
        self.score = 0

    @staticmethod
    def __get_lexicon():
        # Load the lexicon from a JSON file
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def new_game(self):
        # Reset the game with a new prompt (from the same lexicon)
        self.prompt = []
        self.generate_prompt()
        self.input = [Word()]
        self.word_idx = 0
        self.letter_idx = 0
        self.time_remaining = self.GAME_LENGTH
        self.raw_score = 0
        self.incorrect_words = 0
        self.score = 0

    def generate_prompt(self):
        # Generate a prompt of words and store them
        last = ""
        while len(self.prompt) < self.PROMPT_LENGTH:
            choice = random.choice(self.__lexicon)
            if choice != last:  # Avoid back to back words
                self.prompt.append(Word(choice))
                last = choice

    def backspace(self):
        # Delete last letter typed and move cursor back one if not already at the beginning of the prompt
        if self.word_idx == 0 and self.letter_idx == 0:
            return
        elif self.letter_idx == 0:
            self.word_idx -= 1
            self.letter_idx = len(self.input[self.word_idx].char_list)
        else:
            self.input[self.word_idx].remove_last()
            self.letter_idx -= 1

    def get_char(self):
        # Return the character for the current index in the prompt
        if self.word_idx >= len(self.prompt) or self.letter_idx >= len(self.prompt[self.word_idx].char_list):
            return None
        return self.prompt[self.word_idx].char_list[self.letter_idx]

    def type_char(self, ch):
        # Handle keyboard input, update color of letter based on if it was correctly typed and  move the cursor
        if ch == '':
            return
        elif ch == ' ':
            # Move to next word
            self.word_idx += 1
            self.letter_idx = 0
            self.input.append(Word())
        else:
            if self.letter_idx < len(self.prompt[self.word_idx].char_list):
                # Change letter color
                cur_ch = self.get_char()
                if ch == cur_ch.ch:
                    cur_ch.set_correct()
                else:
                    cur_ch.set_incorrect()
                self.input[self.word_idx].add_letter(self.prompt[self.word_idx].char_list[self.letter_idx])
            else:
                self.input[self.word_idx].add_text(ch)
                self.input[self.word_idx].char_list[-1].set_incorrect()
            # Move to next letter
            self.letter_idx += 1

    def tick_timer(self):
        # Count down the game timer by 1 second
        self.time_remaining -= 1

    def end_game(self):
        # Compute the raw and adjusted scores
        words_typed = self.word_idx
        self.raw_score = 60 * words_typed // self.GAME_LENGTH
        self.incorrect_words = self.get_incorrect_words()
        correct_words = words_typed - self.incorrect_words
        self.score = 60 * correct_words // self.GAME_LENGTH

    def get_incorrect_words(self):
        # Compute and return the number of words that were incorrectly typed
        incorrect_words = 0
        for i in range(self.word_idx):
            input_word = self.input[i]
            prompt_word = self.prompt[i]
            if len(input_word.char_list) != len(prompt_word.char_list):
                incorrect_words += 1
                continue
            for j in range(len(prompt_word.char_list)):
                if (input_word.char_list[j] != prompt_word.char_list[j]):
                    incorrect_words += 1
                    continue
        return incorrect_words
