#! /usr/bin/python3
import sys


def parse_input(path):
    elves = set()
    for y, line in enumerate(open(path)):
        for x, char in enumerate(line.strip()):
            if char == '#':
                elves.add((x, y))
    return elves


def iterate(elves, offset):
    targets = {}
    for elf in elves:
        x, y = elf
        directions = [
            {(x - 1, y - 1), (x,     y - 1), (x + 1, y - 1)}, # N
            {(x - 1, y + 1), (x,     y + 1), (x + 1, y + 1)}, # S
            {(x - 1, y - 1), (x - 1, y),     (x - 1, y + 1)}, # W
            {(x + 1, y - 1), (x + 1, y),     (x + 1, y + 1)}, # E
        ]
        target_coords = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        blocked = [elves & directions[i] for i in range(4)]
        if any(blocked):
            for i in range(offset, offset + 4):
                if not blocked[i % 4]:
                    targets.setdefault(target_coords[i % 4], set()).add(elf)
                    break

    any_moves = False
    for target, proposers in targets.items():
        if len(proposers) == 1:
            any_moves = True
            elf = proposers.pop()
            elves.remove(elf)
            elves.add(target)
    return any_moves


def area(elves):
    x0 = min(x for x, y in elves)
    x1 = max(x for x, y in elves)
    y0 = min(y for x, y in elves)
    y1 = max(y for x, y in elves)
    return (x1 - x0 + 1) * (y1 - y0 + 1) - len(elves)
    

def main(input_file):
    elves = parse_input(input_file)
    i = 0
    while iterate(elves, i):
        i += 1
        if i == 10:
            print("Part 1:", area(elves))
    print("Part 2:", i + 1)


if __name__ == '__main__':
    main(sys.argv[1])
