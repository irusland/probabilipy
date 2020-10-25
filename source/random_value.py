from itertools import groupby
from operator import itemgetter

from tabulate import tabulate

from source import random_value_factory, errors


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
            RandomValue.__pow__.__name__: '**',
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
            errors.ProbabilityLackError(s, self.MAX_PROBABILITY)

    def check_probs(self):
        for p in map(lambda p: p[1], self.probability_pairs):
            assert self.MIN_PROBABILITY <= p <= self.MAX_PROBABILITY, \
                errors.TotalProbabilityRangeError(
                    p, self.MIN_PROBABILITY, self.MAX_PROBABILITY
                )

    def __str__(self):
        # todo add Fractions str(Fraction(_[1]))
        x = map(lambda _: _[0], self.probability_pairs)
        p = map(lambda _: str(_[1]), self.probability_pairs)
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
            return random_value_factory.RVFactory(obj).evenly_range(
                obj, obj + 1)
        else:
            raise errors.RandomValueCastError(obj)

    @staticmethod
    def _oper(a: 'RandomValue',
              b: 'RandomValue',
              lx: 'lambda ax, bx: x',
              lp: 'lambda ap, bp: p',
              operation: classmethod = None) -> 'RandomValue':
        try:
            a = RandomValue._try_cast(a)
            b = RandomValue._try_cast(b)
        except errors.RandomValueCastError as e:
            raise errors.RandomValueOperationError(a, b, operation) from e

        pairs = RandomValue._eval(a, b, lx, lp)
        raw = RandomValue._sum_distinct(pairs)

        name = (f'{a.name} '
                f'{a.get_op_sign(operation) if operation else "?"}'
                f' {b.name}')
        if RandomValue.SHOW_PARENTHESES:
            name = ''.join(['(', name, ')'])

        return RandomValue(raw, name=name)

    @staticmethod
    def _values_mul(ax, bx):
        return ax * bx

    @staticmethod
    def _values_add(ax, bx):
        return ax + bx

    @staticmethod
    def _probs_mul(ap, bp):
        return ap * bp

    def __add__(self, other) -> 'RandomValue':
        return self._oper(self, other, self._values_add, self._probs_mul, self.__add__)

    def __radd__(self, other) -> 'RandomValue':
        return self._oper(other, self, self._values_add, self._probs_mul, self.__add__)

    def __mul__(self, other) -> 'RandomValue':
        return self._oper(self, other, self._values_mul, self._probs_mul, self.__mul__)

    def __rmul__(self, other) -> 'RandomValue':
        return self._oper(other, self, self._values_mul, self._probs_mul, self.__mul__)

    def __pow__(self, power, modulo=None) -> 'RandomValue':
        assert modulo is None, NotImplementedError

        rv: RandomValue = self
        for i in range(power - 1):
            rv = self._oper(rv, self, self._values_mul, self._probs_mul)
        name = (f'{self.name} '
                f'{self.get_op_sign(self.__pow__)} '
                f'{power}')
        if RandomValue.SHOW_PARENTHESES:
            name = ''.join(['(', name, ')'])
        rv.name = name
        return rv
