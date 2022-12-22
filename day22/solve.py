#! /usr/bin/python3
import sys
import numpy


# Test cube:
#        ----
#        |20|
#  ----------
#  |01|11|21|
#  -------------
#        |22|32|
#        -------


# My cube:
#      -------
#      |20|30|
#      -------
#      |21|
#   -------
#   |12|22|
#   -------
#   |13|
#   ----


def parse_input(path):
    grid = []
    moves = []
    for line in open(path):
        line = line.rstrip()
        if '.' in line:
            grid.append(line)
        elif line:
            while line:
                l, r = line.find('L'), line.find('R')
                if l == r == -1:
                    moves.append(int(line))
                    break
                i = l if r == -1 else r if l == -1 else min(l, r)
                if i:
                    moves.append(int(line[:i]))
                moves.append(line[i])
                line = line[i + 1:]
    n = max(map(len, grid))
    for i, row in enumerate(grid):
        if len(row) < n:
            grid[i] = row + ' ' * (n - len(row))
    return grid, moves


opposite = {i: (i + 2) % 4 for i in range(4)}
clockwise = {i: (i + 1) % 4 for i in range(4)}
anticlockwise = {i: (i - 1) % 4 for i in range(4)}
forward = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}
class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.pos = (len(self.grid[0]) - len(self.grid[0].lstrip()), 0)
        self.facing = 0

    def lookup(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return ' '

    def turn(self, direction):
        self.facing = {'R': clockwise, 'L': anticlockwise}[direction][self.facing]

    def peek_forward(self):
        xoff, yoff = forward[self.facing]
        new_pos = (self.pos[0] + xoff, self.pos[1] + yoff)
        return new_pos, self.lookup(new_pos)

    def pos_across_edge(self):
        raise NotImplementedError()

    def move_forward(self):
        pos, cell = self.peek_forward()
        facing = self.facing
        if cell == ' ':
            pos, facing = self.pos_across_edge()
            cell = self.lookup(pos)
        if cell != '#':
            self.pos = pos
            self.facing = facing

    def do_the_dance(self, actions):
        for action in actions:
            if isinstance(action, int):
                for _ in range(action):
                    self.move_forward()
            else:
                self.turn(action)
        return 1000 * (self.pos[1] + 1) + 4 * (self.pos[0] + 1) + self.facing


class FlatGrid(Grid):
    def pos_across_edge(self):
        xoff, yoff = forward[self.facing]
        new_pos = (
            (self.pos[0] + xoff) % self.width,
            (self.pos[1] + yoff) % self.height,
        )
        while self.lookup(new_pos) == ' ':
            new_pos = (
                (new_pos[0] + xoff) % self.width,
                (new_pos[1] + yoff) % self.height,
            )
        return new_pos, self.facing


class Cube(Grid):
    def __init__(self, grid):
        super().__init__(grid)
        self.neighbours = self.resolve_faces()

    def resolve_faces(self):
        area = sum(len(row) - row.count(' ') for row in self.grid)
        self.face_len = int((area / 6) ** .5)
        assert 6 * self.face_len ** 2 == area

        faces = {(self.pos[0] // self.face_len, self.pos[1] // self.face_len)}
        done = set()
        neighbours = {}
        def mark_neighbour(_pos, _dir, _neigh, _ndir):
            v = (_neigh, _ndir)
            assert neighbours[_pos].setdefault(_dir, v) == v

        # Pass 1: mark faces which are adjacent on the map
        while faces - done:
            face = (faces - done).pop()
            neighbours.setdefault(face, {})
            for neighbour, dir_ in [
                    ((face[0], face[1] - 1), 3), # up
                    ((face[0], face[1] + 1), 1), # down
                    ((face[0] - 1, face[1]), 2), # left
                    ((face[0] + 1, face[1]), 0), # right
            ]:
                if self.lookup((neighbour[0] * self.face_len, neighbour[1] * self.face_len)) == ' ':
                    continue
                faces.add(neighbour)
                mark_neighbour(face, dir_, neighbour, opposite[dir_])
            done.add(face)

        # Pass 2: mark faces which are adjacent after folding
        while True:
            for face in neighbours:
                for na_dir in range(4):
                    nb_dir = clockwise[na_dir]
                    na = neighbours[face].get(na_dir)
                    nb = neighbours[face].get(nb_dir)
                    if na and nb:
                        na_face, na_side = na
                        nb_face, nb_side = nb
                        mark_neighbour(na_face, anticlockwise[na_side], nb_face, clockwise[nb_side])
                        mark_neighbour(nb_face, clockwise[nb_side], na_face, anticlockwise[na_side])
            if all(len(v) == 4 for v in neighbours.values()):
                break

        return neighbours

    def pos_across_edge(self):
        current_face = (self.pos[0] // self.face_len, self.pos[1] // self.face_len)
        x, y = (self.pos[0] % self.face_len, self.pos[1] % self.face_len)
        S = self.face_len - 1
        new_face, new_side = self.neighbours[current_face][self.facing]
        new_facing = opposite[new_side]

        new_x, new_y = {
            0: {
                1: (y,     x    ), # r -> d
                2: (S - x, y    ), # r -> l
                3: (S - y, S - x), # r -> u
                0: (x,     S - y), # r -> r
            },

            1: {
                2: (S - y, S - x), # d -> l
                3: (x,     S - y), # d -> u
                0: (y,     x    ), # d -> r
                1: (S - x, y    ), # d -> d
            },

            2: {
                3: (y,     x    ), # l -> u
                0: (S - x, y    ), # l -> r
                1: (S - y, S - x), # l -> d
                2: (x,     S - y), # l -> l
            },

            3: {
                0: (S - y, S - x), # u -> r
                1: (x,     S - y), # u -> d
                2: (y,     x    ), # u -> l
                3: (S - x, y    ), # u -> u
            },
        }[self.facing][new_side]

        new_pos = (new_face[0] * self.face_len + new_x,
                   new_face[1] * self.face_len + new_y)

        return new_pos, new_facing

def main(input_file):
    grid, actions = parse_input(input_file)

    print("Part 1:", FlatGrid(grid).do_the_dance(actions))
    print("Part 2:", Cube(grid).do_the_dance(actions))


if __name__ == '__main__':
    main(sys.argv[1])
