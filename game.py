"""
File: game.py

This file contains the typing game logic.
"""
import copy
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
        # Display data
        self.display_prompt = []
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
        """ Load the lexicon from a JSON file 
        :return: The list of words that can be in the prompt
        :rtype: list[str]
        """
        with open("res/lexicon.json", 'r') as f:
            lexicon = json.load(f)
        return lexicon

    def new_game(self):
        """ Reset the game with a new prompt """
        self.prompt = []
        self.generate_prompt()
        self.display_prompt = copy.deepcopy(self.prompt)
        self.input = [Word()]
        self.word_idx = 0
        self.letter_idx = 0
        self.time_remaining = self.GAME_LENGTH
        self.raw_score = 0
        self.incorrect_words = 0
        self.score = 0

    def generate_prompt(self):
        """ Generate a prompt of words and store them """
        last = ""
        while len(self.prompt) < self.PROMPT_LENGTH:
            choice = random.choice(self.__lexicon)
            if choice != last:  # Avoid back to back words
                self.prompt.append(Word(choice))
                last = choice

    def backspace(self):
        """ Delete last letter typed and move cursor back one if not already 
        at the beginning of the prompt 
        """
        if self.word_idx == 0 and self.letter_idx == 0:
            # At beginning of prompt
            return
        elif self.letter_idx == 0:
            # At biginning of word
            self.word_idx -= 1
            self.letter_idx = len(self.input[self.word_idx].char_list)
        else:
            self.input[self.word_idx].remove_last()
            self.letter_idx -= 1

        # Adjust prompt display
        display_word = self.display_prompt[self.word_idx]
        prompt_word = self.prompt[self.word_idx]
        if self.letter_idx >= len(prompt_word.char_list):
            if len(display_word.char_list) > len(prompt_word.char_list):
                display_word.remove_last()
        else:
            display_word.char_list[self.letter_idx].set_default()


    def get_char(self):
        """ Return the character for the current index in the prompt 
        :return: The current character in the prompt
        :rtype: str 
        """
        if self.word_idx < len(self.prompt):
            word = self.prompt[self.word_idx].char_list
            if self.letter_idx < len(word):
                return word[self.letter_idx]
        return None

    def type_char(self, ch):
        """ Handle keyboard input, update color of letter based on if it was 
        correctly typed and move the cursor 
        :param str ch: The character typed
        """
        if ch == ' ':
            # Move to next word
            self.word_idx += 1
            self.letter_idx = 0
            self.input.append(Word())
        elif ch.isalnum():
            dis_word = self.display_prompt[self.word_idx]
            if self.letter_idx < len(self.prompt[self.word_idx].char_list):
                # Update whether char is correct or not
                cur_ch = self.get_char()
                if ch == cur_ch.ch:
                    dis_word.char_list[self.letter_idx].set_correct()
                else:
                    dis_word.char_list[self.letter_idx].set_incorrect()
            else:
                # User added too many characters to word
                dis_word.add_text(ch)
                dis_word.char_list[-1].set_incorrect()
            self.input[self.word_idx].add_text(ch)
            self.letter_idx += 1

    def tick_timer(self):
        """ Count down the game timer by one second """
        self.time_remaining -= 1

    def end_game(self):
        """ Compute the raw and adjusted scores """
        words_typed = self.word_idx
        self.raw_score = 60 * words_typed // self.GAME_LENGTH
        self.incorrect_words = self.get_incorrect_words()
        correct_words = words_typed - self.incorrect_words
        self.score = 60 * correct_words // self.GAME_LENGTH

    def get_incorrect_words(self):
        """ Compute and return the number of words that were incorrectly 
        typed 
        """
        incorrect_words = 0
        for i in range(self.word_idx):
            input_word = self.input[i]
            prompt_word = self.prompt[i]
            if len(input_word.char_list) != len(prompt_word.char_list):
                incorrect_words += 1
                continue
            for j in range(len(prompt_word.char_list)):
                if input_word.char_list[j].ch != prompt_word.char_list[j].ch:
                    incorrect_words += 1
                    break
        return incorrect_words
