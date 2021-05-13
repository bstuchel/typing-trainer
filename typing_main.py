"""
File: typing_main.py

This program runs the typing test application using pygame.

To Do:
 - Add timer and display it on screen
 - Increase word length and wrap text onto next line
 - Add results screen after timer expires
 - Add option to play agains
"""
from game import Game
from gui import Gui
import pygame


def main():
    game = Game()
    gui = Gui(game.get_prompt())
    gui.update_display()

    # Initialize game loop
    running = True
    time_started = False
    cur_idx = 0

    while running:
        if cur_idx == len(gui.prompt.text):
            game.stop_clock()
            raw_wpm = 5/game.get_runtime()*60
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
                if event.unicode == gui.prompt.char_list[cur_idx].ch.lower():
                    # Update the display for correct letter
                    gui.prompt.char_list[cur_idx].set_correct()
                    cur_idx += 1
                else:
                    # Update the display for incorrect letter
                    gui.prompt.char_list[cur_idx].set_incorrect()
                    cur_idx += 1
                gui.update_display()

    pygame.quit()


if __name__ == '__main__':
    main()
