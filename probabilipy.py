from tabulate import tabulate
from itertools import groupby
from operator import itemgetter


class ProbabilityBaseError(Exception):
    def __init__(self, actual, message):
        self.message = f'Probability {actual}: {message}'
        super().__init__(self.message)


class ProbabilityLackError(ProbabilityBaseError):
    def __init__(self, actual, expected=None):
        self.message = f'did not match {expected}'
        super().__init__(actual, self.message)


class TotalProbabilityRangeError(ProbabilityBaseError):
    def __init__(self, actual, min_expected, max_expected):
        self.message = f'was not in range [{min_expected},{max_expected}]'
        super().__init__(actual, self.message)


class RandomValueOperationError(Exception):
    def __init__(self, this: 'RandomValue', other, operation):
        self.message = (
            f'Cannot apply {operation} between\n'
            f'\t{this} of type {type(this)} and\n'
            f'\t{other} of type {type(other)}'
        )
        super().__init__(self.message)


class RandomValue:
    MAX_PROBABILITY = 1
    MIN_PROBABILITY = 0

    def __init__(self, probability_pairs: list, name='random value'):
        self.probability_pairs = probability_pairs
        self.validate()
        self.name = name
        self._size = len(probability_pairs)

    def size(self):
        return self._size

    def validate(self):
        self.check_probs()
        self.check_prob_sum()

    def check_prob_sum(self):
        s = sum(map(lambda p: p[1], self.probability_pairs))
        eps = 1e-7
        if abs(s - self.MAX_PROBABILITY) > eps:
            raise ProbabilityLackError(s, self.MAX_PROBABILITY)

    def check_probs(self):
        for p in map(lambda p: p[1], self.probability_pairs):
            if self.MIN_PROBABILITY <= p <= self.MAX_PROBABILITY:
                pass
            else:
                raise TotalProbabilityRangeError(p, self.MIN_PROBABILITY,
                                                 self.MAX_PROBABILITY)

    def __str__(self):
        x = map(lambda _: _[0], self.probability_pairs)
        p = map(lambda _: _[1], self.probability_pairs)
        s = (
            f'{self.name}:',
            tabulate([p], x, tablefmt="grid"),
        )
        return '\n'.join(s)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.probability_pairs}, "{self.name}")'

    @staticmethod
    def _sum_distinct(pairs):
        first = itemgetter(0)
        return [(k, sum(item[1] for item in tups_to_sum))
                for k, tups_to_sum in
                groupby(sorted(pairs, key=first), key=first)]

    @staticmethod
    def _eval(a: 'RandomValue',
              b: 'RandomValue',
              lx: 'lambda ax, bx: x',
              lp: 'lambda ap, bp: p', ) -> 'RandomValue':
        pairs = []
        for ax, ap in a.probability_pairs:
            for bx, bp in b.probability_pairs:
                pairs.append((lx(ax, bx), lp(ap, bp)))
        return RandomValue(RandomValue._sum_distinct(pairs))

    @staticmethod
    def _oper(a: 'RandomValue',
              b: 'RandomValue',
              lx: 'lambda ax, bx: x',
              lp: 'lambda ap, bp: p',
              operation) -> 'RandomValue':
        if isinstance(b, RandomValue):
            pass
        elif isinstance(b, int):
            b = RVFactory.evenly_range(b, b + 1)
        else:
            raise RandomValueOperationError(a, b, operation)
        return RandomValue._eval(a, b, lx, lp)

    def __add__(self, other) -> 'RandomValue':
        lx = lambda ax, bx: (ax + bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(self, other, lx, lp, self.__add__)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other) -> 'RandomValue':
        lx = lambda ax, bx: (ax * bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(self, other, lx, lp, self.__add__)

    def __rmul__(self, other):
        return self * other


class RVFactory:
    @staticmethod
    def range(probability, start, stop, step=1):
        return RandomValue(
            [(i, probability) for i in range(start, stop, step)])

    @staticmethod
    def evenly_range(start, stop, step=1):
        return RVFactory.range(1 / (stop - start), start, stop, step)

    @staticmethod
    def arrange(values: list, probabilities: list):
        return RandomValue([(x, p) for (x, p) in zip(values, probabilities)])


def main():
    ksi = RVFactory.evenly_range(1, 7)
    print(ksi.__repr__())
    print(ksi.__str__())
    mu = RVFactory.arrange(
        [0,     1],
        [2/3,   1/3],
    )
    print(mu.__repr__())
    print(mu.__str__())

    print(2*ksi + mu + 3)

    print('.............................')


if __name__ == '__main__':
    main()
