#! /usr/bin/python3
import sys


def do_moves(moves, rope_len):
    xs = [0] * rope_len
    ys = [0] * rope_len
    visited = { (xs[-1], ys[-1]) }

    for (mx, my), distance in moves:
        for _ in range(distance):
            xs[0] += mx
            ys[0] += my
            for i in range(rope_len - 1):
                dx = xs[i + 1] - xs[i]
                dy = ys[i + 1] - ys[i]
                if abs(dx) == 2 or abs(dy) == 2:
                    xs[i + 1] = xs[i] + int(dx / 2)
                    ys[i + 1] = ys[i] + int(dy / 2)
            visited.add( (xs[-1], ys[-1]) )

    return len(visited)


def main(input_file):
    offsets = {'L': (-1, 0), 'R': (1, 0), 'D': (0, -1), 'U': (0, 1)}
    moves = [(offsets[line[0]], int(line[1:])) for line in open(input_file)]
    print("Part 1:", do_moves(moves, 2))
    print("Part 2:", do_moves(moves, 10))


if __name__ == '__main__':
    main(sys.argv[1])
