import pygame
import time


def timer_setup(window, timer, colors, fonts, run_time):
    buffer = 10  # pixels between edges
    pressed = pygame.key.get_pressed()  # gets pressed keys

    # ------------------------------------------------------------------------------------------------------------- #

    if not timer["timing"]:  # if the timer is not started yet
        txt_color = colors["gray"]
        color = colors["light_red"]
        if pressed[pygame.K_SPACE] == 1:  # if space bar is pressed and held
            timer["countdown"] += 1
            if timer["countdown"] > 15:
                color = colors["light_green"]
                txt_color = colors["light_green"]
            else:
                color = colors["light_red"]
                txt_color = colors["light_red"]

        elif pressed[pygame.K_SPACE] == 0:  # resets count if space bar is released
            if timer["countdown"] > 15:
                color = colors["light_green"]  # if space bar is held for bit starts timer and changes and color
                timer["timing"] = True
                timer["start_time"] = round(abs((run_time - time.time())), 2)

            elif timer["countdown"] != 15:
                timer["countdown"] = 0
                color = colors["light_yellow"]  # maintains hand color when space bar isn't held consistently
                txt_color = colors["gray"]

# ------------------------------------------------------------------------------------------------------------- #

        pygame.draw.circle(window, color, (455, 71), 50)  # draws circles where hands will be placed
        pygame.draw.circle(window, color, (747, 71), 50)

        left_hand = pygame.image.load('left_hand.png')  # loads images of hands
        right_hand = pygame.image.load('right_hand.png')

        window.blit(left_hand, (415 + buffer, 15 + buffer))  # draws images of hands to the screen
        window.blit(right_hand, (695 + buffer, 15 + buffer))

        txt = fonts["regular"].render(str(timer["solve_time"]), True, txt_color)  # displays previous time
        window.blit(txt, (555, 50))  # draws to screen

    else:
        if pressed[pygame.K_SPACE] == 1:  # when timer is stopped
            timer["timing"] = False
            timer["countdown"] = 0
            log_time(timer)  # tracks time in time.txt file


def start_timing(timer, run_time):

    if timer["timing"]:  # if timing
        time_now = time.time()  # starts timing and calculates solve time
        timer["solve_time"] = round(round(abs((run_time - time_now)), 2) - timer["start_time"], 2)


def log_time(timer):
    file = open("times.txt", "a")  # opens file in appending mode
    value = (str(timer["solve_time"]) + "\n")  # formats value for storing

    file.write(value)  # appends solve time into file
    file.close()  # closes file
