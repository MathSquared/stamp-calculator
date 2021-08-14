#!/usr/bin/env python3

from collections import namedtuple
from decimal import Decimal
import re


def nbr(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][n] if n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] else str(n)


def qty(n, sing, pl):
    return (sing if n == 1 else pl).format(n=nbr(n))


Result = namedtuple('Result', ['size', 'overage', 'stamps'])


class Stamp:
    def __init__(self, value, name=None):
        self._value = value
        self._name = name

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def __str__(self):
        if self.name:
            return f'{self.name} ({self.value})'
        else:
            return f'({self.value})'

    def __repr__(self):
        return f'Stamp({self.value!r}, {self.name!r})'


def compute(found, trace, stamps, goal, cap, num):
    # found and trace are modified over the course of the recursion.
    if cap < 0:
        return
    if goal <= 0:
        overage = -goal
        found.append(Result(size=len(trace), overage=overage, stamps=tuple(trace)))
        return
    if num <= 0: # and goal > 0; i.e., if this isn't a solution
        return
    for i, stamp in enumerate(stamps):
        trace.append(stamp)
        # with the recursive call, exclude more expensive stamps; we already considered them
        compute(found, trace, stamps[i:], goal - stamp.value, cap - stamp.value, num - 1)
        trace.pop()
    return found


def read_stamps():
    # Returns a list sorted descending by value.
    stamps = []
    value_prog = re.compile(r'[0-9]+\.[0-9]*|\.?[0-9]+')
    while True:
        line = input('STAMP --> ')
        if not line:
            stamps.sort(key=lambda stamp: -stamp.value)
            return stamps
        value, _, name = line.partition(' ')
        if value_prog.fullmatch(value):
            stamps.append(Stamp(Decimal(value), name))
        else:
            print('ERROR: Please enter a value, optionally followed by a space and a name.')


def main():
    print('Welcome to the Stamp Calculator.')
    print()
    goal = Decimal(input('How much value do you need to add up to?        GOAL AMOUNT --> '))
    cap = Decimal(input('How much value do you not want to exceed?        CAP AMOUNT --> '))
    num = Decimal(input('What\'s the most number of stamps you will use?   MAX STAMPS --> '))
    print()
    print('Enter the values of your stamps, one per line.')
    print('You can also include names for your stamps, separated from the value by a space.')
    print('Enter an empty line when you\'re done.')
    stamps = read_stamps()
    results = compute([], [], stamps, goal, cap, num)
    results.sort(key=lambda result: (result.size, result.overage))

    print()
    last_size = None
    for result in results:
        if result.size != last_size:
            print()
            print(qty(result.size, 'With {n} stamp:', 'With {n} stamps:'))
        last_size = result.size
        print('{:8f} - {}'.format(goal + result.overage, ' + '.join(str(stamp) for stamp in result.stamps)))


if __name__ == '__main__':
    main()
