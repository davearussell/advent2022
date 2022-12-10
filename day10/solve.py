#! /usr/bin/python3
import sys


def run(ops):
    x = 1
    values = []
    for op in ops:
        values.append(x)
        if op is not None:
            values.append(x)
            x += op
    return [(t + 1, value) for t, value in enumerate(values)]


def render(values):
    grid = [[' '] * 40 for _ in range(6)]
    for cycle, value in values:
        row, col = divmod(cycle - 1, 40)
        if abs(value - col) <= 1:
            grid[row][col] = '█'
    return '\n'.join(''.join(row) for row in grid)


def main(input_file):
    ops = [
        None if 'noop' in line else int(line.split()[-1])
        for line in open(input_file)
    ]
    values = run(ops)
    print("Part 1:", sum(t * x for (t, x) in values[19::40]))
    print("Part 2:\n" + render(values))


if __name__ == '__main__':
    main(sys.argv[1])
