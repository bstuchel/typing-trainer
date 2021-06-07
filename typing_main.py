"""
File: typing_main.py

This program runs the typing test application using pygame.

To Do:
 - The game should load more text if the end of the prompt is reached
 - Add cursor
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

    game = Game()
    gui = Gui()
    game_state = GameState.GAME

    while True:
        if game_state == GameState.GAME:
            game_state = play(game, gui)

        if game_state == GameState.SCORE:
            game_state = score(gui)

        if game_state == GameState.QUIT:
            pygame.quit()
            return        

def play(game, gui):
    game.new_game()
    gui.set_game(game)

    # Initialize game loop
    time_started = False
    chars_typed = ""

    # Game loop
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                # Change game state to QUIT
                return GameState.QUIT

            if event.type == TIME_EVENT:
                # One second has passed, update timer
                game.tick_timer()
                gui.update_timer()
                if game.time_remaining <= 0:
                    # Move to SCORE game state
                    pygame.time.set_timer(TIME_EVENT, 0)
                    game.end_game(chars_typed)
                    gui.display_score(game.score)
                    return GameState.SCORE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    game.prev_char()
                    game.get_char().set_default()
                    gui.update_prompt()
                    chars_typed = chars_typed[:-1]

                elif event.unicode != '':
                    chars_typed += event.unicode
                    # The key pressed was a character
                    if not time_started:
                        # Start the game timer
                        pygame.time.set_timer(TIME_EVENT, 1000)
                        time_started = True
                    
                    # Update wether the letter was correctly typed
                    if event.unicode == game.get_char().ch:
                        game.get_char().set_correct()
                    else:
                        game.get_char().set_incorrect()

                    # Update display
                    gui.update_prompt()
                    game.next_char()

def score(gui):
    # Display results screen
    gui.display_score()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Change game state to QUIT
                return GameState.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return GameState.GAME


if __name__ == '__main__':
    main()
