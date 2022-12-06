#! /usr/bin/python3
import sys


def find_marker(data, marker_len):
    seq = []
    for i, char in enumerate(data):
        if char in seq:
            seq = seq[seq.index(char) + 1:]
        seq.append(char)
        if len(seq) == marker_len:
            return i + 1


def main(input_file):
    data = open(input_file).read().strip()
    print(find_marker(data, 4))
    print(find_marker(data, 14))


if __name__ == '__main__':
    main(sys.argv[1])
