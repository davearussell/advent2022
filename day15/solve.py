#! /usr/bin/python3
import sys


def parse_input(path):
    sensors = []
    for line in open(path):
        sx, sy, bx, by = [
            int(x.split('=')[1].rstrip(',:'))
            for x in line.split()
            if '=' in x
        ]
        sensors.append(((sx, sy), (bx, by)))
    return sensors


def merge_ranges(ranges):
    ranges.sort()
    overlaps = []
    merged = [ranges[0]]
    for thisl, thisr in ranges[1:]:
        prevl, prevr = merged[-1]
        if thisr <= prevr: # this sits entirely within prev
            pass
        elif thisl == prevl: # prev sits entirely within this
            merged[-1] = (thisl, thisr)
        elif thisl <= prevr + 1: # ranges can be merged
            overlaps.append(prevr - thisl + 1)
            merged[-1] = (prevl, thisr)
        else: # ranges do not overlap
            merged.append((thisl, thisr))
    return merged, min(overlaps) if overlaps else None


def get_coverage(sensors, y):
    """ """
    ranges = []
    for (sx, sy), (bx, by) in sensors:
        coverage = abs(sx - bx) + abs(sy - by)
        ydist = abs(sy - y)
        if ydist > coverage:
            continue
        ranges.append((sx - (coverage - ydist),
                       sx + (coverage - ydist)))

    return merge_ranges(ranges)


def count_known_empty(sensors, y):
    coverage = get_coverage(sensors, y)[0]
    known_empty = 0
    beacons = {bx for _, (bx, by) in sensors if by == y}
    for l, r in coverage:
        n_beacons = len([b for b in beacons if l <= b <= r])
        known_empty += r - l + 1 - n_beacons
    return known_empty


def find_gap(sensors, minval, maxval):
    y = minval
    while True:
        ranges, internal_overlap = get_coverage(sensors, y)
        for l, r in ranges:
            if r < minval:
                continue
            if r < maxval:
                return 4000000 * (r + 1) + y
            if l > minval:
                return 4000000 * (l - 1) + y
            overlap = min(minval - l, r - maxval)
            break

        if internal_overlap:
            overlap = min(overlap, (internal_overlap + 1) // 2)
        y += overlap


def main(input_file):
    sensors = parse_input(input_file)
    print("Part 1:", count_known_empty(sensors, 2000000))
    print("Part 2:", find_gap(sensors, 0, 4000000))


if __name__ == '__main__':
    main(sys.argv[1])
