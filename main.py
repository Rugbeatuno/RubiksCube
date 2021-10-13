import pygame
import time

from graph import graph_setup, graph_lines
from timer import timer_setup, start_timing
from stats import stats
from sidebar import display_times



pygame.init()  # initializes imported library

# screen
screen_width, screen_height = 1200, 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rubik's Cube Timer")

# colors
colors = {"white": (255, 255, 240), "black": (0, 0, 0), "light_green": (120, 220, 60),
          "light_red": (250, 100, 100), "light_yellow": (240, 240, 60), "yellow": (240, 240, 100),
          "gray": (100, 100, 100), "light_gray": (230, 230, 230), "purple": (150, 0, 120),
          "green": (0, 120, 0), "orange": (250, 150, 100)}

# timer
timer = {"countdown": 0, "solve_time": 0.00, "timing": False, "start_time": None}
run_time = time.time()

# graph
graph = {"worst": 0, "best": 0, "nums": [], "time_range": [], "scale": 10}

# fonts
fonts = {"regular": pygame.font.Font(None, 65),
         "big": pygame.font.Font(None, 130),
         "small": pygame.font.Font(None, 40),
         "tiny": pygame.font.Font(None, 30)}


def redraw_window(window):
    pygame.display.update()  # updates/refreshes screen
    window.fill(colors["white"])  # draws screen background white

    if not timer["timing"]:
        pygame.draw.line(window, colors["black"], (400, 0), (400, screen_height))  # separates screen into 3 sections
        pygame.draw.line(window, colors["black"], (800, 0), (800, screen_height))
    else:
        txt = fonts["big"].render(str(timer["solve_time"]), True, (100, 100, 100))  # displays time
        window.blit(txt, (520, 235))

    timer_setup(window, timer, colors, fonts, run_time)  # sets up timers colors and images
    start_timing(timer, run_time)  # starts timer if conditions met

    stats(window, timer, graph, fonts, colors)  # shows statistics for solves

    graph_setup(window, graph, colors, fonts)  # draws actual graph and info
    graph_lines(window, graph, colors, timer)  # calls graphs lines from graph.py



def reset_times(window):
    mouse_pos = pygame.mouse.get_pos()  # gets mouse coordinates and when clicked
    mouse_clicked = pygame.mouse.get_pressed()
    color = colors["light_gray"]
    if not timer["timing"]:
        if 550 < mouse_pos[0] < 650 and 540 < mouse_pos[1] < 570:  # if mouse xy is over the rest button
            color = colors["light_green"]  # hover color is green
            if mouse_clicked[0]:  # and if it is clicked resets all times
                file = open("times.txt", "w")
                file.write("")
                file.close()

        pygame.draw.rect(window, color, (550, 540, 100, 30))  # draws reset time button and text
        reset_txt = fonts["small"].render(str("Reset"), True, colors["black"])
        window.blit(reset_txt, (563, 543))


def main():
    run = True
    FPS = 50  # frames/sec
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():  # when user exits program
            if event.type == pygame.QUIT:
                run = False  # stops running

        redraw_window(win)  # redraws window
        reset_times(win)
        display_times(win, colors, fonts)


main()  # calls main loop
pygame.QUIT()
