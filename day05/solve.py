#! /usr/bin/python3
import copy
import sys


def parse_input(path):
    stacks = {}
    moves = []
    for line in open(path):
        if line.startswith('move'):
            moves.append([int(x) for x in line.split()[1::2]])
        elif line.strip():
            for i, char in enumerate(line[1::4]):
                if char.isalpha():
                    stacks.setdefault(i + 1, []).insert(0, char)
    return stacks, moves


def main(input_file):
    stacks, moves = parse_input(input_file)
    p1_stacks = copy.deepcopy(stacks)
    p2_stacks = copy.deepcopy(stacks)

    for n, src, dst in moves:
        p1_stacks[dst] += [p1_stacks[src].pop() for i in range(n)]
        p2_stacks[dst] += reversed([p2_stacks[src].pop() for i in range(n)])
    print(''.join(p1_stacks[k][-1] for k in sorted(p1_stacks)))
    print(''.join(p2_stacks[k][-1] for k in sorted(p2_stacks)))


if __name__ == '__main__':
    main(sys.argv[1])
