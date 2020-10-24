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


class RandomValueCastError(Exception):
    def __init__(self, other):
        self.message = (
            f'Cannot cast {other} of type {type(other)} to {type(RandomValue)}'
        )
        super().__init__(self.message)


class RandomValue:
    MAX_PROBABILITY = 1
    MIN_PROBABILITY = 0
    OPSIGNS = None
    SHOW_PARENTHESES = True

    def __init__(self, probability_pairs: list, name='random value'):
        self.probability_pairs = probability_pairs
        self.validate()
        self.name = name
        self._size = len(probability_pairs)
        RandomValue.OPSIGNS = {
            RandomValue.__add__.__name__: '+',
            RandomValue.__mul__.__name__: '*',
        }

    def size(self):
        return self._size

    def validate(self):
        self.check_probs()
        self.check_prob_sum()

    def check_prob_sum(self):
        s = sum(map(lambda p: p[1], self.probability_pairs))
        eps = 1e-7
        assert abs(s - self.MAX_PROBABILITY) <= eps, \
            ProbabilityLackError(s, self.MAX_PROBABILITY)

    def check_probs(self):
        for p in map(lambda p: p[1], self.probability_pairs):
            assert self.MIN_PROBABILITY <= p <= self.MAX_PROBABILITY, \
                TotalProbabilityRangeError(
                    p, self.MIN_PROBABILITY, self.MAX_PROBABILITY
                )

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

    def get_op_sign(self, op: classmethod):
        if op.__name__ in self.OPSIGNS:
            return self.OPSIGNS[op.__name__]

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
              lp: 'lambda ap, bp: p', ):
        pairs = []
        for ax, ap in a.probability_pairs:
            for bx, bp in b.probability_pairs:
                pairs.append((lx(ax, bx), lp(ap, bp)))
        return pairs

    @staticmethod
    def _try_cast(obj) -> 'RandomValue':
        if isinstance(obj, RandomValue):
            return obj
        elif isinstance(obj, int):
            return RVFactory(obj).evenly_range(obj, obj + 1)
        else:
            raise RandomValueCastError(obj)

    @staticmethod
    def _oper(a: 'RandomValue',
              b: 'RandomValue',
              lx: 'lambda ax, bx: x',
              lp: 'lambda ap, bp: p',
              operation: classmethod) -> 'RandomValue':
        try:
            a = RandomValue._try_cast(a)
            b = RandomValue._try_cast(b)
        except RandomValueCastError as e:
            raise RandomValueOperationError(a, b, operation) from e

        pairs = RandomValue._eval(a, b, lx, lp)
        raw = RandomValue._sum_distinct(pairs)

        name = f'{a.name} {a.get_op_sign(operation)} {b.name}'
        if RandomValue.SHOW_PARENTHESES:
            name = ''.join(['(', name, ')'])

        return RandomValue(raw, name=name)

    def __add__(self, other) -> 'RandomValue':
        lx = lambda ax, bx: (ax + bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(self, other, lx, lp, self.__add__)

    def __radd__(self, other):
        lx = lambda ax, bx: (ax + bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(other, self, lx, lp, self.__add__)

    def __mul__(self, other) -> 'RandomValue':
        lx = lambda ax, bx: (ax * bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(self, other, lx, lp, self.__mul__)

    def __rmul__(self, other):
        lx = lambda ax, bx: (ax * bx)
        lp = lambda ap, bp: (ap * bp)
        return self._oper(other, self, lx, lp, self.__mul__)

    def _expected_value(self) -> int:
        pass

    def _covariance(self) -> int:
        pass

    def _statistical_dispersion(self) -> int:
        pass


def E(rv: RandomValue):
    """Мат ожидание"""
    return rv._expected_value()


def D(rv: RandomValue):
    """Дисперсия"""
    return rv._covariance()


def Cov(rv: RandomValue):
    """Коваривация"""
    return rv._covariance()


class RVFactory:
    RV_NAME = 'Random Value from factory'

    def __init__(self, name):
        RVFactory.RV_NAME = name

    @staticmethod
    def range(probability, start, stop, step=1):
        return RandomValue(
            [(i, probability) for i in range(start, stop, step)],
            name=RVFactory.RV_NAME
        )

    @staticmethod
    def evenly_range(start, stop, step=1):
        return RVFactory.range(1 / (stop - start), start, stop, step)

    @staticmethod
    def arrange(values: list, probabilities: list):
        assert len(values) == len(probabilities)
        return RandomValue(
            [(x, p) for (x, p) in zip(values, probabilities)],
            name=RVFactory.RV_NAME
        )


def main():
    ksi = RVFactory('ξ').evenly_range(1, 7)
    print(ksi.__repr__())
    print(ksi.__str__())
    mu = RVFactory('μ').arrange(
        [0, 1],
        [2 / 3, 1 / 3],
    )
    print(mu.__repr__())
    print(mu.__str__())
    print(2 * ksi + mu + 3)

    print('.............................')
    ksi = RVFactory('ξ').arrange(
        [-1, 0, 1],
        [1 / 3, 1 / 3, 1 / 3]
    )
    print(ksi)
    print(ksi * ksi)
    print(ksi * ksi * ksi)
    print(ksi * ksi * ksi * ksi)


if __name__ == '__main__':
    main()
