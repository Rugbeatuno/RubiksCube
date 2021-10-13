import pygame


def graph_setup(window, graph, colors, fonts):
    file = open("times.txt", "r")
    lines = len(file.readlines())  # gets number of solves
    nums = graph["nums"]  # times from previous solves (newest 25)
    gap = 60  # gap between graphed lines

# -------------------------------------------------------------------------------------------- #
# This section draws the graph and number of solves (x-axis)

    pygame.draw.rect(window, colors["purple"], (850, 130, 50, 50))  # creates key for colored graph
    pygame.draw.rect(window, colors["orange"], (850, 190, 50, 50))

    solve_time_txt = fonts["small"].render(str("Solve Time (secs)"), True, colors["black"])  # creates text
    running_avg_txt = fonts["small"].render(str("Running Average"), True, colors["black"])
    window.blit(solve_time_txt, (920, 140))
    window.blit(running_avg_txt, (920, 200))  # displays text

    for i in range(10):
        pygame.draw.line(window, colors["light_gray"], (850, 250 + i * gap), (1150, 250 + i * gap))  # draws horizontal graph lines
    for i in range(6):
        pygame.draw.line(window, colors["light_gray"], (850 + i * gap, 250), (850 + i * gap, 550))  # draws vertical graph lines
    pygame.draw.line(window, colors["black"], (850, 550), (1150, 550))

    if lines >= 25:  # draws number of solves
        nums = [i for i in range(lines - 25, lines + 1, 5)]
    elif lines < 25:
        nums = [0, 5, 10, 15, 20, 25]
    for i in enumerate(nums):  # generates text
        txt_x = fonts["tiny"].render(str(i[1]), True, colors["black"])
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
        txt_y = fonts["tiny"].render(str(i[1]), True, colors["black"])  # renders text
        x = 810
        y = 250 + gap * i[0] 
        window.blit(txt_y, (x, y))  # displays text

    file.close()


def graph_lines(window, graph, colors, timer):
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
        pygame.draw.line(window, colors["purple"], (start_x, start_y), (start_x, end_y), 7)

        solve_time = timer["solve_time"]

        x, y = 850 + gap * 2 + (i[0]) * gap, 550
        current_y = y - round(float(solve_time * pixel))

        if float(timer["solve_time"]) < float(graph["best"]):  # changes line color based on current time
            color = colors["green"]  # green for faster than personal best
        elif timer["solve_time"] > graph["worst"]:
            color = colors["light_red"]  # red for slower than worst
        else:
            color = colors["yellow"]  # yellow for in between

        if len(lines) - 1 == i[0] and timer["timing"]:  # draws the line while solving
            if current_y >= 250:
                pygame.draw.line(window, color, (x, y), (x, current_y), 7)  # draws line

    if len(lines) < 1 and timer["timing"]:  # if it is the first solve
        x, y = 850 + gap, 550  # calculates starting x and y cords
        current_y = y - round(float(timer["solve_time"] * pixel))  # finds the height
        pygame.draw.line(window, colors["green"], (x, y), (x, current_y), 7)  # draws line

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

        pygame.draw.line(window, colors["orange"], (x1, y1), (x2, y2), 7)  # draws line based on points given

    file.close()  # closes file
