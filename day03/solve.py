#! /usr/bin/python3
import string
import sys
from functools import reduce


def main(input_file):
    packs = []
    for line in open(input_file):
        line = line.strip()
        n = len(line) // 2
        packs.append([set(line[:n]), set(line[n:])])

    p1_items = [(a & b).pop() for (a, b) in packs]
    p2_items = [
        reduce(set.__and__, [a | b for (a, b) in packs[i:i+3]]).pop()
        for i in range(0, len(packs), 3)
    ]

    prios = dict(zip(string.ascii_letters, range(1, 53)))
    print(sum(prios[item] for item in p1_items))
    print(sum(prios[item] for item in p2_items))


if __name__ == '__main__':
    main(sys.argv[1])
