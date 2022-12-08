#! /usr/bin/python3
import sys


def visible_trees(row, rev=False):
    seen = -1
    for i, tree in reversed(list(enumerate(row))) if rev else enumerate(row):
        if tree > seen:
            yield i
            seen = tree


def view_distance(trees):
    d = 0
    for tree in trees[1:]:
        d += 1
        if tree >= trees[0]:
            break
    return d


def scenic_score(grid, x, y):
    dist_left = view_distance([grid[y][i] for i in range(x, -1, -1)])
    dist_right = view_distance([grid[y][i] for i in range(x, len(grid))])
    dist_up = view_distance([grid[j][x] for j in range(y, -1, -1)])
    dist_down = view_distance([grid[j][x] for j in range(y, len(grid))])
    return dist_left * dist_right * dist_up * dist_down


def count_visible_trees(grid):
    visible = set()
    for i, row in enumerate(grid):
        col = [grid[j][i] for j in range(len(grid))]
        visible |= {(x, i) for x in visible_trees(row)}           # from left
        visible |= {(x, i) for x in visible_trees(row, rev=True)} # from right
        visible |= {(i, y) for y in visible_trees(col)}           # from top
        visible |= {(i, y) for y in visible_trees(col, rev=True)} # from bottom
    return len(visible)


def find_best_tree(grid):
    r = range(1, len(grid) - 1) # skip edges since they're all 0
    return max(scenic_score(grid, x, y) for x in r for y in r)


def main(input_file):
    grid = [
        [int(char) for char in line.strip()]
        for line in open(input_file)
    ]
    assert len(grid) == len(grid[0])
    print("Part 1:", count_visible_trees(grid))
    print("Part 2:", find_best_tree(grid))


if __name__ == '__main__':
    main(sys.argv[1])
