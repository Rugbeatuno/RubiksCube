import pygame

num_range = [0]
def display_times(win, colors, fonts):
    file = open("times.txt", "r")
    lines = file.readlines()

    solves = {}

    for i in enumerate(lines):  # cycles through all times
        if num_range[0] <= i[0] <= num_range[0] + 11:
            time = i[1]
            time = time[:-1]
            solve_num = i[0]
            solves[solve_num] = float(time)  # stores in dictionary

    pygame.draw.rect(win, colors["black"], (50, 190, 300, 360), 1)  # draws box where times will be displayed
    for i in enumerate(solves):
        if i[0] == 0:
            pygame.draw.rect(win, colors["gray"], (51, 191, 298, 28))  # draws gray box around newest time

        x, y = 53, 194 + i[0] * 30  # calculates where to place numbers

        solve_num = i[0]
        solve_time = solves[solve_num]


        solve_num_txt = fonts["tiny"].render((str(solve_num + 1) + "."), True, colors["black"])  # formats solve#
        win.blit(solve_num_txt, (x, y))

        solve_time_txt = fonts["tiny"].render(str(solve_time), True, colors["black"])  # formats times
        win.blit(solve_time_txt, (x + 150, y))  # displays text

# --------------------------------------------------------------------------------- #
    mouse_pos = pygame.mouse.get_pos()
    if 50 < mouse_pos[0] < 350 and 190 < mouse_pos[1] < 550:  # while mouse is in sidebar
        for event in pygame.event.get():  # gets mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and num_range[0] > 0:  # when scrolling up
                    num_range[0] -= 1
                elif event.button == 5 and num_range[0] + 12 < len(lines):  # when scrolling down
                    num_range[0] += 1
