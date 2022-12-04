#! /usr/bin/python3
import sys


def main(input_file):
    pairs = [
        [[int(x) for x in word.split('-')] for word in line.split(',')]
        for line in open(input_file)
    ]

    contains = overlaps = 0
    for (a, b), (c, d) in pairs:
        if (a >= c and b <= d) or (a <= c and b >= d):
            contains += 1
        if (b >= c and a <= d):
            overlaps += 1
    print(contains)
    print(overlaps)


if __name__ == '__main__':
    main(sys.argv[1])
