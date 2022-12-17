#! /usr/bin/python3
import sys

import numpy
from numba import njit


_ROCKS = [
    [
        0b0011110,
    ],

    [
        0b0001000,
        0b0011100,
        0b0001000,
    ],

    [
        0b0011100,
        0b0000100,
        0b0000100,
    ],

    [
        0b0010000,
        0b0010000,
        0b0010000,
        0b0010000,
    ],

    [
        0b0011000,
        0b0011000,
    ],
]
ROCKS = [numpy.array(l, dtype=numpy.int16) for l in _ROCKS]


def row_to_str(row):
    s = '|'
    for i in range(7):
        s += ('#' if row & (1 << (6 - i)) else ' ')
    return  s + '|'


def dump_room(room):
    s = ''
    for row in room[::-1]:
        s += row_to_str(row) + '\n'
    print(s + '-' * 9)


@njit(cache=True)
def move(room, rock, y, offset):
    if offset == 1 and numpy.any(rock & 1):
        return rock
    if offset == -1 and numpy.any(rock & 0b1000000):
        return rock

    moved = rock.copy()
    if offset == 1:
        moved >>= 1
    else:
        moved <<= 1

    for i in range(len(rock)):
        if len(room) <= y + i:
            break
        if moved[i] & room[y + i]:
            return rock

    return moved

@njit(cache=True)
def can_drop(room, rock, y):
    if not y:
        return False
    for rock_row, room_row in zip(rock, room[y - 1:]):
        if rock_row & room_row:
            return False
    return True


@njit(cache=True)
def place_rock(room, rock, y):
    for i in range(len(rock)):
        if len(room) <= y + i:
            room = numpy.append(room, numpy.int16(0))
        assert not room[i + y] & rock[i]
        room[i + y] |= rock[i]
    return room


@njit(cache=True)
def drop_rock(room, jets, jet_i, rock):
    y = len(room) + 3
    while True:
        rock = move(room, rock, y, jets[jet_i])
        jet_i = (jet_i + 1) % len(jets)
        if not can_drop(room, rock, y):
            break
        y -= 1
    return place_rock(room, rock, y), jet_i


@njit(cache=True)
def drop_rocks(room, jets, jet_i, rocks, rock_i, n):
    for i in range(n):
        rock = rocks[rock_i]
        rock_i = (rock_i + 1) % len(rocks)
        room, jet_i = drop_rock(room, jets, jet_i, rock)
    return room, jet_i, rock_i


def main(input_file):
    data = open(input_file).read().strip()
    cycle_len = len(data) * len(ROCKS)

    jets = numpy.array([{'<': -1, '>': +1}[symbol] for symbol in data], dtype=numpy.int16)
    jet_i = 0

    rocks = tuple(ROCKS)
    rock_i = 0

    room = numpy.zeros(0, dtype=numpy.int16)

    #for j in range(2022):
    #    room = drop_rock(room, jets, next(rocks))
    #print("Part 1:", len(room))
    #return

    target = 2132455

    after_one = None
    height = 0
    room_len = 0
    n_rocks = 0
    n = 0
    while True:
        count = cycle_len # 13345 if n == 0 else cycle_len
        room, jet_i, rock_i = drop_rocks(room, jets, jet_i, rocks, rock_i, count)

        full = numpy.where(room == 127)[0][-1]
        height += (len(room) - room_len)
        room = room[full + 1:]
        room_len = len(room)
        n_rocks += count
        n += 1
        print("Done %d cycles (%d rocks), height=%d, room len=%d" % (n, n_rocks, height, len(room)))
        if after_one is None:
            after_one = room.copy()
        elif numpy.array_equal(room, after_one):
            print("  Time has repeated")


# One cycle = n_rock_type x jet_sequence_len = 50455
# State repeats after 348 cycles
# After 2 cycles, height is 155450
# Every 347 cycles after that add 26973243

# C = 50455
# N = 2 * C
# D = 347 * C
# HD = 26973243
# T = 1000000000000
# N + xD + y == T
# x, y =  divmod(T - N, D)

# To get the final count, we simulate the first N + y rocks then add x * HD
# N + y comes out at 3285320
# Final answer is 3285320 + 57117 * 26973243 = 1540634005751


if __name__ == '__main__':
    main(sys.argv[1])
