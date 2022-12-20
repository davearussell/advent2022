#! /usr/bin/python3
import sys
import numpy
import numba


@numba.njit(cache=True)
def swapr(vs, ls, rs, i, n):
    il = ls[i]
    ir = rs[i]
    nl = i
    for _ in range(n):
        nl = rs[nl]
    nr = rs[nl]

    rs[il] = ir
    ls[ir] = il
    rs[nl] = i
    ls[nr] = i
    ls[i] = nl
    rs[i] = nr


@numba.njit(cache=True)
def mix(vs, ls, rs):
    for i in range(len(vs)):
        shift = vs[i] % (len(vs) - 1)
        if shift:
            swapr(vs, ls, rs, i, shift)


def make_ring(values):
    vs = numpy.array(values, dtype=numpy.int64)
    ls = numpy.zeros(len(values), dtype=numpy.int64)
    rs = numpy.zeros(len(values), dtype=numpy.int64)
    for i in range(len(values)):
        ls[i] = (i - 1) % len(values)
        rs[i] = (i + 1) % len(values)
    return vs, ls, rs


def score(vs, ls, rs):
    score = 0
    i = numpy.where(vs == 0)[0][0]
    for j in range(3000):
        i = rs[i]
        if j % 1000 == 999:
            score += vs[i]
    return score


def main(input_file):
    values = [int(x) for x in open(input_file).read().split()]

    vs, ls, rs = make_ring(values)
    mix(vs, ls, rs)
    print("Part 1:", score(vs, ls, rs))

    vs, ls, rs = make_ring([v * 811589153 for v in values])
    for _ in range(10):
        mix(vs, ls, rs)
    print("Part 2:", score(vs, ls, rs))


if __name__ == '__main__':
    main(sys.argv[1])
