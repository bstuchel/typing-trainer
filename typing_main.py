"""
File: typing_main.py

This program runs the typing test application using pygame.

To Do:
 - Add cursor
 - Add timer and display it on screen
 - Show results on screen after timer expires
 - Add option to play again
"""
from game import Game
from gui import Gui
import pygame


def main():
    game = Game()
    gui = Gui(game)

    # Initialize game loop
    running = True
    time_started = False
    cur_idx = 0

    while running:
        if cur_idx == len(game.prompt_text):
            game.stop_clock()
            raw_wpm = game.prompt_size/game.get_runtime()*60
            print("Raw WPM: %6.2f" % raw_wpm)
            running = False

        for event in pygame.event.get():
            # End loop if window is closed
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not time_started:
                    # Start game timer
                    game.start_clock()
                    time_started = True
                if event.key == pygame.K_BACKSPACE:
                    # Update the display for a backspace
                    gui.char_list[cur_idx-1].set_default()
                    gui.update_display(cur_idx-1)
                    if cur_idx != 0: cur_idx -= 1
                elif event.unicode == game.prompt_text[cur_idx]:
                    # Update the display for correct letter
                    gui.char_list[cur_idx].set_correct()
                    cur_idx += 1
                elif event.unicode != '':
                    # Update the display for incorrect letter
                    gui.char_list[cur_idx].set_incorrect()
                    cur_idx += 1
                gui.update_display(cur_idx-1)

    pygame.quit()


if __name__ == '__main__':
    main()
