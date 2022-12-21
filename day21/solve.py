#! /usr/bin/python3
import sys
import operator


class Value:
    def __init__(self, n):
        self.n = n

    def eval(self):
        return self.n


class Expr:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.fn = {'+': operator.add,
                   '-': operator.sub,
                   '*': operator.mul,
                   '/': operator.floordiv}[op]
        self.rhs = rhs

    def eval(self):
        return self.fn(self.lhs.eval(), self.rhs.eval())


def parse_input(path):
    vars = {}
    for line in open(path).read().strip().split('\n'):
        var, expr = line.split(': ')
        if expr.isdigit():
            vars[var] = Value(int(expr))
        else:
            vars[var] = Expr(*expr.split())
    for expr in vars.values():
        if isinstance(expr, Expr):
            expr.lhs = vars[expr.lhs]
            expr.rhs = vars[expr.rhs]
    return vars['root'], vars['humn']


def gradient(equation, x):
    x0 = x
    v0 = equation(x)
    while (v1 := equation(x)) == v0:
        x += 1
    return (v1 - v0) / (x - x0)


def solve_equation(equation):
    x = 0
    while True:
        if not (y := equation(x)):
            return x
        x -= int(y / gradient(equation, x))


def main(input_file):
    root, humn = parse_input(input_file)

    print("Part 1:", root.eval())
    
    def equation(x):
        humn.n = x
        return root.lhs.eval() - root.rhs.eval()
    print("Part 2:", solve_equation(equation))


if __name__ == '__main__':
    main(sys.argv[1])
