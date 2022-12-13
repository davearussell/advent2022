#! /usr/bin/python3
import functools
import sys


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return -1 if a < b else 0 if a == b else 1
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    for ai, bi in zip(a, b):
        if (n := compare(ai, bi)):
            return n
    return compare(len(a), len(b))


def main(input_file):
    packets = [eval(line) for line in open(input_file) if line.strip()]

    pairs = zip(packets[::2], packets[1::2])
    in_order = [i for i, (a, b) in enumerate(pairs) if compare(a, b) == -1]
    print("Part 1:", sum([i + 1 for i in in_order]))

    divs = [ [[2]], [[6]] ]
    p2 = sorted(packets + divs, key=functools.cmp_to_key(compare))
    print("Part 2:", (p2.index(divs[0]) + 1) * (p2.index(divs[1]) + 1))


if __name__ == '__main__':
    main(sys.argv[1])
