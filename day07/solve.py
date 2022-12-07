#! /usr/bin/python3
import sys


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subdirs = []
        self.files = []

    @property
    def size(self):
        return sum(d.size for d in self.subdirs + self.files)

    def walk(self):
        yield self
        for subdir in self.subdirs:
            yield from subdir.walk()


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def parse_input(path):
    root = Dir('/')
    cwd = root
    for line in open(path):
        line = line.strip()
        if line.startswith('$ cd '):
            target = line[len('$ cd '):]
            if target == '..':
                cwd = cwd.parent
            elif target == '/':
                cwd = root
            else:
                cwd = [d for d in cwd.subdirs if d.name == target][0]
        elif not line.startswith('$'):
            attr, name = line.split()
            if attr == 'dir':
                cwd.subdirs.append(Dir(name, cwd))
            else:
                cwd.files.append(File(name, int(attr)))
    return root


def main(input_file):
    tree = parse_input(input_file)

    small_dirs = [d for d in tree.walk() if d.size <= 100000]
    print("Part 1:", sum(d.size for d in small_dirs))

    req_space = 30000000 - (70000000 - tree.size)
    candidates = [d for d in tree.walk() if d.size >= req_space]
    candidates.sort(key=lambda d: d.size)
    print("Part 2:", candidates[0].size)


if __name__ == '__main__':
    main(sys.argv[1])
