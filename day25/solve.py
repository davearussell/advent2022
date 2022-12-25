#! /usr/bin/python3
import sys

d_to_s = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}
s_to_d = {v: k for k, v in d_to_s.items()}


class Snafu:
    def __init__(self, x):
        if isinstance(x, int):
            self.v = x
        else:
            self.v = 0
            for i, digit in enumerate(x[::-1]):
                self.v += (5 ** i) * s_to_d[digit]

    def __add__(self, other):
        v2 = other if isinstance(other, int) else other.v
        return type(self)(self.v + v2)

    def __repr__(self):
        v = self.v
        digits = []
        while v:
            v, digit = divmod(v, 5)
            digits.append(digit)
        for i in range(len(digits)):
            if digits[i] > 2:
                digits[i] -= 5
                if i == len(digits) - 1:
                    digits.append(1)
                else:
                    digits[i + 1] += 1
        return ''.join(d_to_s[digit] for digit in digits[::-1])


def main(input_file):
    values = open(input_file).read().split()
    print("Part 1:", sum(map(Snafu, values), Snafu(0)))


if __name__ == '__main__':
    main(sys.argv[1])
