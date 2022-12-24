#! /usr/bin/python3
import math
import sys


def parse_input(path):
    grid = []
    for line in open(path):
        grid.append(line.strip())
    start_x = [i for i, c in enumerate(grid[0]) if c == '.'][0]
    goal_x = [i for i, c in enumerate(grid[-1]) if c == '.'][0]
    grid = [line[1:-1] for line in grid[1:-1]]
    assert(start_x == 1 and goal_x == len(grid[0]))
    return grid, (0, -1), (len(grid[0]) - 1, len(grid))


def identify_safe_cells(grid, start, goal):
    width = len(grid[0])
    height = len(grid)
    period = math.lcm(width, height)
    winds = []
    directions = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
    all_cells = {(x, y) for x in range(width) for y in range(height)} | {start, goal}
    safe_cells = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in '<>^v':
                winds.append([(x, y), directions[cell]])

    for i in range(period):
        wind_cells = {pos for pos, _ in winds}
        safe_cells.append(all_cells - wind_cells)
        for wind in winds:
            x, y = wind[0]
            dx, dy = wind[1]
            wind[0] = ((x + dx) % width, (y + dy) % height)

    return safe_cells


def plot_course(safe_cells, start, goal, t):
    period = len(safe_cells)
    possible_cells = {start}
    while True:
        t += 1
        targets = set()
        for x, y in possible_cells:
            destinations = {(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
            safe_destinations = destinations & safe_cells[t % period]
            if goal in safe_destinations:
                return t
            targets |= safe_destinations
        possible_cells = targets


def main(input_file):
    grid, start, goal = parse_input(input_file)
    safe_cells = identify_safe_cells(grid, start, goal)
    t1 = plot_course(safe_cells, start, goal, 0)
    t2 = plot_course(safe_cells, goal, start, t1)
    t3 = plot_course(safe_cells, start, goal, t2)
    print("Part 1:", t1)
    print("Part 2:", t3)


if __name__ == '__main__':
    main(sys.argv[1])
