#! /usr/bin/python3
import sys


def neighbours(point, minv, maxv):
    x, y, z = point
    candidates = set()
    if x > minv:
        candidates.add((x - 1, y, z))
    if x < maxv:
        candidates.add((x + 1, y, z))
    if y > minv:
        candidates.add((x, y - 1, z))
    if y < maxv:
        candidates.add((x, y + 1, z))
    if z > minv:
        candidates.add((x, y, z - 1))
    if z < maxv:
        candidates.add((x, y, z + 1))
    return candidates


def main(input_file):
    droplet = {
        tuple(int(x) for x in line.split(','))
        for line in open(input_file)
         if ',' in line
    }
    minv = min(min(point) for point in droplet) - 1
    maxv = max(max(point) for point in droplet) + 1

    area = 6 * len(droplet)
    for point in droplet:
        area -= len(neighbours(point, minv, maxv) & droplet)
    print("Part 1:", area)


    part2_area = 0
    frontier = [(minv, minv, minv)]
    steam = {frontier[0]}
    while frontier:
        point = frontier.pop()
        for other in neighbours(point, minv, maxv) - steam:
            if other in droplet:
                part2_area += 1
            else:
                steam.add(other)
                frontier.append(other)
    print("Part 2:", part2_area)


if __name__ == '__main__':
    main(sys.argv[1])
