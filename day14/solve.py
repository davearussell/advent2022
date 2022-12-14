#! /usr/bin/python3
import copy
import sys


def make_grid(walls):
    maxy = max(y1 for ((x0, y0), (x1, y1)) in walls)
    grid = {}
    for ((x0, y0), (x1, y1)) in walls:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                grid[(x, y)] = 1
    return grid, maxy + 2


def parse_input(path):
    walls = []
    for line in open(path):
        if not line.strip():
            continue
        x0 = y0 = None
        for coord in line.split('->'):
            x1, y1 = map(int, coord.split(','))
            if x0 is not None:
                if x0 > x1:
                    walls.append( ((x1, y0), (x0, y1)) )
                elif y0 > y1:
                    walls.append( ((x1, y1), (x0, y0)) )
                else:
                    walls.append( ((x0, y0), (x1, y1)) )
            x0, y0, = x1, y1
    return make_grid(walls)


def inject_sand(grid, bottom, floor=False):
    x, y = 500, 0
    if grid.get((x, y)):
        return False
    while y < bottom:
        if floor and y == bottom - 1:
            grid[(x, y)] = 2
            return True
        for nx in [x, x - 1, x + 1]:
            if not grid.get((nx, y + 1)):
                y += 1
                x = nx
                break
        else:
            grid[(x, y)] = 2
            return True
    return False


def count_sand(_grid, bottom, floor=False):
    grid = copy.deepcopy(_grid)
    n = 0
    while inject_sand(grid, bottom, floor):
        n += 1
    return n


def main(input_file):
    grid, bottom = parse_input(input_file)
    print("Part 1:", count_sand(grid, bottom, False))
    print("Part 2:", count_sand(grid, bottom, True))


if __name__ == '__main__':
    main(sys.argv[1])
