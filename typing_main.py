"""
File: typing_main.py

This program runs the typing test application using pygame.

To Do:
 - End game when timer reaches 0 (rather than after the promp has been typed)
 - Add cursor
 - Show results on screen after timer expires
 - Add option to play again
"""
from game import Game
from gui import Gui
import pygame
# pygame.init()

TIME_EVENT = pygame.USEREVENT

def main():
    game = Game()
    gui = Gui(game)

    # Initialize game loop
    running = True
    time_started = False
    cur_idx = 0

    while running:
        if cur_idx == len(game.prompt_text):
            # End of prompt reached
            print("You finished")
            running = False

        for event in pygame.event.get():
            # End loop if window is closed
            if event.type == pygame.QUIT:
                running = False

            if event.type == TIME_EVENT:
                # One second has passed, update timer
                game.tick_timer()
                gui.update_timer()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if cur_idx != 0: cur_idx -= 1
                    gui.char_list[cur_idx].set_default()
                    gui.update_prompt(cur_idx)

                elif event.unicode != '':
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

                    # Update display and move to the next letter
                    gui.update_prompt(cur_idx)
                    cur_idx += 1

    pygame.quit()


if __name__ == '__main__':
    main()
