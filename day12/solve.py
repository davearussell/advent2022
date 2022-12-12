#! /usr/bin/python3
import heapq
import string
import sys


def parse_input(path):
    """
    Returns (grid, graph, start_point, goal_point)

    graph is represented as a dict mapping each point (x, y)
    to the list of points from which that point is accessible
    """
    grid = [line.strip() for line in open(path)]
    graph = {}
    width, height = len(grid[0]), len(grid)
    start = goal = None
    elevation = dict(zip(string.ascii_lowercase, range(26)))
    elevation.update({'S': elevation['a'], 'E': elevation['z']})
    for y in range(height):
        for x in range(width):
            graph[(x, y)] = []
            cell = grid[y][x]
            if cell == 'S':
                start = (x, y)
                continue
            if cell == 'E':
                goal = (x, y)
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < width and 0 <= ny < height:
                    if elevation[grid[ny][nx]] - elevation[cell] >= -1:
                        graph[(x, y)].append((nx, ny))
    return grid, graph, start, goal


def find_paths(graph, goal):
    """Returns a dict mapping each point on the grid to the number of steps
    required to move from that point to the goal."""
    q = [(0, goal)]
    path_lengths = {goal: 0}
    while q:
        cost, current = heapq.heappop(q)
        for point in graph[current]:
            if point not in path_lengths or cost + 1 < path_lengths[point]:
                path_lengths[point] = cost + 1
                heapq.heappush(q, (cost + 1, point))
    return path_lengths


def main(input_file):
    grid, graph, start, goal = parse_input(input_file)
    path_lengths = find_paths(graph, goal)
    min_length = min(l for (x, y), l in path_lengths.items()
                    if grid[y][x] in 'aS')
    print("Part 1:", path_lengths[start])
    print("Part 2:", min_length)


if __name__ == '__main__':
    main(sys.argv[1])
