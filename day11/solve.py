#! /usr/bin/python3
import copy
import sys
import yaml
from functools import reduce


def parse_op(text):
    assert text.startswith('new = '), text
    lhs, op, rhs = text[len('new = '):].split()
    def f(old):
        l = old if lhs == 'old' else int(lhs)
        r = old if rhs == 'old' else int(rhs)
        return l + r if op == '+' else l * r
    return f


def parse_input(path):
    raw_monkeys = yaml.safe_load(open(path).read().replace('  If', 'If'))
    monkeys = []
    for name, spec in raw_monkeys.items():
        assert int(name.split()[-1]) == len(monkeys), name
        monkeys.append({
            'items': [int(x) for x in str(spec['Starting items']).split(', ')],
            'op': parse_op(spec['Operation']),
            'divisor': int(spec['Test'].split()[-1]),
            'true': int(spec['If true'].split()[-1]),
            'false': int(spec['If false'].split()[-1]),
        })
    return monkeys


def do_monkey_business(_monkeys, n_rounds, relief_factor):
    monkeys = copy.deepcopy(_monkeys)
    counts = [0] * len(_monkeys)
    modulus = reduce(int.__mul__, [monkey['divisor'] for monkey in monkeys])
    for x in range(n_rounds):
        for i, monkey in enumerate(monkeys):
            for item in monkey['items']:
                counts[i] += 1
                item = (monkey['op'](item) // relief_factor) % modulus
                result = 'false' if item % monkey['divisor'] else 'true'
                monkeys[monkey[result]]['items'].append(item)
            monkey['items'] = []
    counts.sort()
    return counts[-2] * counts[-1]


def main(input_file):
    monkeys = parse_input(input_file)
    print("Part 1:", do_monkey_business(monkeys, 20, 3))
    print("Part 2:", do_monkey_business(monkeys, 10000, 1))


if __name__ == '__main__':
    main(sys.argv[1])
