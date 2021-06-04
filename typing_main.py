"""
File: typing_main.py

This program runs the typing test application using pygame.

To Do:
 - The game should load more text if the end of the prompt is reached
 - Add cursor
 - Add option to play again
"""
from enum import Enum
from game import Game
from gui import Gui
import pygame

TIME_EVENT = pygame.USEREVENT

class GameState(Enum):
    QUIT = -1
    GAME = 0
    SCORE = 1

def main():
    pygame.init()

    gui = Gui()
    game_state = GameState.GAME

    while True:
        if game_state == GameState.GAME:
            game_state = play(gui)

        if game_state == GameState.SCORE:
            game_state = score(gui)

        if game_state == GameState.QUIT:
            pygame.quit()
            return        

def play(gui):
    game = Game()
    gui.set_game(game)

    # Initialize main loop
    time_started = False
    cur_idx = 0
    chars_typed = ""

    # Main loop
    while True:

        for event in pygame.event.get():
            # End loop if window is closed
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == TIME_EVENT:
                # One second has passed, update timer
                game.tick_timer()
                gui.update_timer()
                if game.time_remaining <= 0:
                    game.end_game(chars_typed)
                    gui.display_score(game.score)
                    return GameState.SCORE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if cur_idx != 0: cur_idx -= 1
                    gui.char_list[cur_idx].set_default()
                    gui.update_prompt(cur_idx)
                    if chars_typed:
                        chars_typed = chars_typed[:-1]

                elif event.unicode != '':
                    chars_typed += event.unicode
                    # The key pressed was a character
                    if not time_started:
                        # Start the game timer
                        pygame.time.set_timer(TIME_EVENT, 1000)
                        time_started = True
                    
                    # Update wether the letter was correctly typed
                    if event.unicode == game.prompt_text[cur_idx]:
                        gui.char_list[cur_idx].set_correct()
                    else:
                        gui.char_list[cur_idx].set_incorrect()

                    # Update display
                    gui.update_prompt(cur_idx)
                    cur_idx += 1

    pygame.quit()


if __name__ == '__main__':
    main()
