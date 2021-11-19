"""
File: main.py

This program runs the typing test application using pygame.
"""
from enum import Enum
from game import Game
from gui import Gui
import pygame

TIME_EVENT = pygame.USEREVENT


class GameState(Enum):
    # Type used to control the gamestate
    QUIT = -1
    GAME = 0
    SCORE = 1


def main():
    """ Set up contronl and flow of the application """
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
    """ Start the typing test game
    :param game.Game game: Game object
    :param gui.Gui gui: Gui object
    :return: The game state upon quitting application or finishing the game
    :rtype: GameState
    """
    game.new_game()
    gui.set_game(game)
    time_started = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == TIME_EVENT:
                # One second has passed, update timer
                game.tick_timer()
                if game.time_remaining <= 0:
                    # Game over
                    pygame.time.set_timer(TIME_EVENT, 0)
                    game.end_game()
                    gui.display_score()
                    return GameState.SCORE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    game.backspace()
                else:
                    if not time_started:
                        # Start the game timer
                        pygame.time.set_timer(TIME_EVENT, 1000)
                        time_started = True
                    game.type_char(event.unicode)

            gui.update_display()


def score(gui):
    """ Display the results screen
    :param gui.Gui gui: Gui object
    :return: The game state upon quitting application or starting new game
    :rtype: GameState
    """
    gui.display_score()

    # Result screen loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return GameState.GAME


if __name__ == '__main__':
    main()
