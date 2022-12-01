#! /usr/bin/python3
import sys


def main(input_file):
    elves = [[]]
    for line in open(input_file):
        if line.strip():
            elves[-1].append(int(line))
        else:
            elves.append([])

    sums = sorted(sum(elf) for elf in elves)
    print(sums[-1])
    print(sum(sums[-3:]))


if __name__ == '__main__':
    main(sys.argv[1])
