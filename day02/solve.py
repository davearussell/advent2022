#! /usr/bin/python3
import sys


def p1_score(them, us):
    return us + 1 + ((us + 1 - them) % 3) * 3


def p2_score(them, outcome):
    return p1_score(them, (them + outcome - 1) % 3)


def main(input_file):
    plays = []
    decode = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}
    for line in open(input_file):
        plays.append([decode[word] for word in line.split()])
    print(sum(p1_score(*play) for play in plays))
    print(sum(p2_score(*play) for play in plays))


if __name__ == '__main__':
    main(sys.argv[1])
