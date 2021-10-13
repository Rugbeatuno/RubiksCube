import pygame

def stats(window, timer, graph, fonts, colors):
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
        pygame.draw.line(window, colors["black"], (400, 130), (800, 130))  # draws separation lines
        pygame.draw.line(window, colors["black"], (400, 340), (800, 340))

        graph["best"] = PB[0]
        best = fonts["small"].render(str("Best: " + str(PB[0])), True, colors["black"])  # displays best time
        window.blit(best, (530, 150))

        graph["worst"] = PB[-1]  # saves worst time for graphing
        worst = fonts["small"].render(str("Worst: " + str(PB[-1])), True, colors["black"])  # displays worst time
        window.blit(worst, (512, 200))

        total = 0
        for i in PB:  # calculates sum of all times in times.txt file
            total += i
        get_average = round(total / len(PB), 2)
        average = fonts["small"].render(str("Average: " + str(get_average)), True, colors["black"])  # displays average time
        window.blit(average, (479, 250))

        get_median = PB[round(len(PB) / 2)]
        median = fonts["small"].render(str("Median: " + str(get_median)), True, colors["black"])  # displays median time
        window.blit(median, (490, 300))

        average_of_5 = fonts["small"].render((str("Avg of 5: " + str(total_5))), True, colors["black"])  # displays average of past 5 solves
        window.blit(average_of_5, (481, 360))

        average_of_12 = fonts["small"].render((str("Avg of 12: " + str(total_12))), True, colors["black"])  # displays average of past 12 solves
        window.blit(average_of_12, (466, 410))

    file.close()  # closes file