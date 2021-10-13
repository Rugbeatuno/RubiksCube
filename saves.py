'''import pygame
import time

pygame.init()  # initializes pygame

# screen
screen_width, screen_height = 1200, 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rubik's Cube Timer")

# colors
white = (255, 255, 240)
black = (0, 0, 0)
light_green = (120, 220, 60)
light_red = (250, 100, 100)
light_yellow = (240, 240, 60)
yellow = (240, 240, 100)
gray = (100, 100, 100)
light_gray = (230, 230, 230)
purple = (150, 0, 120)
green = (0, 120, 0)
orange = (250, 150, 100)

# timer
timer = {"countdown": 0, "solve_time": 0.00, "timing": False, "start_time": None}
run_time = time.time()

# fonts
font = pygame.font.Font(None, 65)
big_font = pygame.font.Font(None, 130)
small_font = pygame.font.Font(None, 40)
tiny_font = pygame.font.Font(None, 30)

# graph
graph = {"buffer": 50, "gap": 60, "worst": 0, "best": 0, "nums": [], "time_range": [], "scale": 10}


def redraw_window(window):
    pygame.display.update()  # updates/refreshes screen
    window.fill(white)  # draws screen background white

    if not timer["timing"]:
        pygame.draw.line(window, black, (400, 0), (400, screen_height))  # separates screen into 3 sections
        pygame.draw.line(window, black, (800, 0), (800, screen_height))
    else:
        txt = big_font.render(str(timer["solve_time"]), True, (100, 100, 100))  # displays time
        window.blit(txt, (520, 235))

    timer_setup(window)  # draws timer
    stats(window)  # shows statistics
    graph_setup(window)  # draws graph
    graph_lines(window)  # draws graph lines


def timer_setup(window):
    buffer = 10  # pixels between edges
    pressed = pygame.key.get_pressed()  # gets pressed keys

    # ------------------------------------------------------------------------------------------------------------- #

    if not timer["timing"]:  # if the timer is not started yet
        txt_color = gray
        color = light_red
        if pressed[pygame.K_SPACE] == 1:  # if space bar is pressed and held
            timer["countdown"] += 1
            if timer["countdown"] > 15:
                color = light_green
                txt_color = light_green
            else:
                color = light_red
                txt_color = light_red

        elif pressed[pygame.K_SPACE] == 0:  # resets count if space bar is released
            if timer["countdown"] > 15:
                color = light_green  # if space bar is held for bit starts timer and changes and color
                timer["timing"] = True
                timer["start_time"] = round(abs((run_time - time.time())), 2)

            elif timer["countdown"] != 15:
                timer["countdown"] = 0
                color = light_yellow  # maintains hand color when space bar isn't held consistently
                txt_color = gray

# ------------------------------------------------------------------------------------------------------------- #

        pygame.draw.circle(window, color, (455, 71), 50)  # draws circles where hands will be placed
        pygame.draw.circle(window, color, (747, 71), 50)

        left_hand = pygame.image.load('left_hand.png')  # loads images of hands
        right_hand = pygame.image.load('right_hand.png')

        window.blit(left_hand, (415 + buffer, 15 + buffer))  # draws images of hands to the screen
        window.blit(right_hand, (695 + buffer, 15 + buffer))

        txt = font.render(str(timer["solve_time"]), True, txt_color)  # displays previous time
        win.blit(txt, (555, 50))  # draws to screen

    else:
        if pressed[pygame.K_SPACE] == 1:  # when timer is stopped
            timer["timing"] = False
            timer["countdown"] = 0
            log_time()  # tracks time in time.txt file


def start_timing():

    if timer["timing"]:  # if timing
        time_now = time.time()  # starts timing and calculates solve time
        timer["solve_time"] = round(round(abs((run_time - time_now)), 2) - timer["start_time"], 2)


def log_time():
    file = open("times.txt", "a")  # opens file in appending mode
    value = (str(timer["solve_time"]) + "\n")  # formats value for storing

    file.write(value)  # appends solve time into file
    file.close()  # closes file


def stats(window):
    file = open("times.txt", 'r')  # opens file to read mode
    total_solves = file.readlines()  # grabs all stored solves
    # PB = personal best

    lines = []  # stores all times
    for i in total_solves:  # copies file data into list
        lines.append(i)

    PB = [x[:-1] for x in lines]  # removes \n from the end of each line
    for i in range(0, len(PB)):
        PB[i] = float(PB[i])  # changes str values in list into int values

    total_5 = 0
    total_12 = 0
    if len(PB) >= 12:  # gets average of past 12 solves
        avg_12 = PB[-12:]
        for i in avg_12:
            total_12 += i
        total_12 /= 12
        total_12 = round(total_12, 2)  # rounds value to hundredths place

    if len(PB) >= 5:  # gets average of past 5 solves before list is sorted
        avg_5 = PB[-5:]
        for i in avg_5:
            total_5 += i
        total_5 /= 5
        total_5 = round(total_5, 2)  # rounds value

    PB.sort()  # sorts lists based on time

    if not timer["timing"]:
        if len(total_solves) >= 1:
            pass
        else:
            PB = [0]
        pygame.draw.line(window, black, (400, 130), (800, 130))  # draws separation lines
        pygame.draw.line(window, black, (400, 340), (800, 340))

        graph["best"] = PB[0]
        best = small_font.render(str("Best: " + str(PB[0])), True, black)  # displays best time
        win.blit(best, (530, 150))

        graph["worst"] = PB[-1]  # saves worst time for graphing
        worst = small_font.render(str("Worst: " + str(PB[-1])), True, black)  # displays worst time
        win.blit(worst, (512, 200))

        total = 0
        for i in PB:  # calculates sum of all times in times.txt file
            total += i
        get_average = round(total / len(PB), 2)
        average = small_font.render(str("Average: " + str(get_average)), True, black)  # displays average time
        win.blit(average, (479, 250))

        get_median = PB[round(len(PB) / 2)]
        median = small_font.render(str("Median: " + str(get_median)), True, black)  # displays median time
        win.blit(median, (490, 300))

        average_of_5 = small_font.render((str("Avg of 5: " + str(total_5))), True, black)  # displays average of past 5 solves
        win.blit(average_of_5, (481, 360))

        average_of_12 = small_font.render((str("Avg of 12: " + str(total_12))), True, black)  # displays average of past 12 solves
        win.blit(average_of_12, (466, 410))

    file.close()  # closes file


def graph_setup(window):
    file = open("times.txt", "r")
    lines = len(file.readlines())  # gets number of solves
    nums = graph["nums"]  # times from previous solves (newest 25)
    buffer = graph["buffer"]  # distance from edges
    gap = graph["gap"]  # gap between graphed lines

# -------------------------------------------------------------------------------------------- #
# This section draws the graph and number of solves (x-axis)

    pygame.draw.rect(window, purple, (850, 130, 50, 50))  # creates key for colored graph
    pygame.draw.rect(window, orange, (850, 190, 50, 50))

    solve_time_txt = small_font.render(str("Solve Time (secs)"), True, black)  # creates text
    running_avg_txt = small_font.render(str("Running Average"), True, black)
    window.blit(solve_time_txt, (920, 140))
    window.blit(running_avg_txt, (920, 200))  # displays text

    for i in range(10):
        pygame.draw.line(window, light_gray, (800 + buffer, 250 + i * gap), (1200 - buffer, 250 + i * gap))  # draws horizontal graph lines
    for i in range(6):
        pygame.draw.line(window, light_gray, (800 + buffer + i * gap, 250), (800 + buffer + i * gap, 550))  # draws vertical graph lines
    pygame.draw.line(window, black, (800 + buffer, 600 - buffer), (1200 - buffer, 600 - buffer))

    if lines >= 25:  # draws number of solves
        nums = [i for i in range(lines - 25, lines + 1, 5)]
    elif lines < 25:
        nums = [0, 5, 10, 15, 20, 25]
    for i in enumerate(nums):  # generates text
        txt_x = tiny_font.render(str(i[1]), True, black)
        x = 850 + i[0] * gap
        y = 560
        window.blit(txt_x, (x, y))  # displays number of solves text

# -------------------------------------------------------------------------------------------- #
# This section scales the time based on your worst time
    worst = graph["worst"]
    worst = int(round(worst/5) * 5)

    if worst < 50:
        graph["time_range"] = [i for i in range(0, 51, 10)]  # sets range from 0-50 by increments of 10
    else:
        graph["scale"] = round(worst/4)  # sets range based on worst time
        graph["time_range"] = [i for i in range(0, worst + graph["scale"] + 2, graph["scale"])]  # appends values to list

    graph["time_range"].sort(reverse=True)  # sorts list from greatest to smallest

    for i in enumerate(graph["time_range"]):
        txt_y = tiny_font.render(str(i[1]), True, black)  # renders text
        x = 810
        y = 250 + gap * i[0]
        window.blit(txt_y, (x, y))  # displays text

    file.close()


def graph_lines(window):
    file = open("times.txt", "r")
    lines = file.readlines()
    solves = [i[:-1] for i in lines]
    pixel = 60 / graph["scale"]  # if solves is greater than 25, grabs the newest 25 solves
    gap = 12  # distance between graphed lines

# -------------------------------------------------------------------------------------------- #
# This section graphs the vertical lines that show the duration of solves

    if len(solves) <= 25:  # if number of solves is less than 25
        pass
    else:
        solves = solves[-25:]

    for i in enumerate(solves):  # cycles throughout and draws graph
        start_x, start_y = 850 + gap + i[0] * gap, 550
        end_y = start_y - round(float(i[1]) * pixel)
        pygame.draw.line(window, purple, (start_x, start_y), (start_x, end_y), 7)

        solve_time = timer["solve_time"]

        x, y = 850 + gap * 2 + (i[0]) * gap, 550
        current_y = y - round(float(solve_time * pixel))

        if float(timer["solve_time"]) < float(graph["best"]):  # changes line color based on current time
            color = green  # green for faster than personal best
        elif timer["solve_time"] > graph["worst"]:
            color = light_red  # red for slower than worst
        else:
            color = yellow  # yellow for in between

        if len(lines) - 1 == i[0] and timer["timing"]:  # draws the line while solving
            if current_y >= 250:
                pygame.draw.line(window, color, (x, y), (x, current_y), 7)  # draws line

    if len(lines) < 1 and timer["timing"]:  # if it is the first solve
        x, y = 850 + gap, 550  # calculates starting x and y cords
        current_y = y - round(float(timer["solve_time"] * pixel))  # finds the height
        pygame.draw.line(window, green, (x, y), (x, current_y), 7)  # draws line

    # -------------------------------------------------------------------------------------------- #
# This section calculates the average times of the previous solves

    times = [x[:-1] for x in lines]  # removes \n from the end of each line
    averages = []  # stores averages
    avg_x = []
    avg_y = []

    total = 0
    for i in range(len(times)):  # goes through all a solves
        total += float(times[i])  # adds next solve time to previous times
        avg = round(float(total / (i + 1)), 2)  # gets sum of all times divided by number of solves
        averages.append(avg)  # adds average time to list
# -------------------------------------------------------------------------------------------- #
# This section draws the average times of the previous solves using several lines at each point

    if len(averages) <= 25:
        pass
    else:
        averages = averages[-25:]  # picks newest 25 averages

    for i in enumerate(averages):
        avg_x.append(850 + gap + i[0] * gap)  # finds x and y cords based on scale
        avg_y.append(550 - round(i[1] * pixel))

    for i in range(len(avg_x) - 1):
        x1 = avg_x[i]
        x2 = avg_x[i+1]  # gets starting and ending points for average line
        y1 = avg_y[i]
        y2 = avg_y[i+1]

        pygame.draw.line(window, orange, (x1, y1), (x2, y2), 7)  # draws line based on points given

    file.close()  # closes file


def reset_times(window):
    mouse_pos = pygame.mouse.get_pos()  # gets mouse coordinates and when clicked
    mouse_clicked = pygame.mouse.get_pressed()
    color = light_gray
    if not timer["timing"]:
        if 550 < mouse_pos[0] < 650 and 540 < mouse_pos[1] < 570:  # if mouse xy is over the rest button
            color = light_green  # hover color is green
            if mouse_clicked[0]:  # and if it is clicked resets all times
                file = open("times.txt", "w")
                file.write("")
                file.close()

        pygame.draw.rect(window, color, (550, 540, 100, 30))  # draws reset time button and text
        reset_txt = small_font.render(str("Reset"), True, black)
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
        start_timing()
        reset_times(win)


main()  # calls main loop
pygame.QUIT()'''



