from tabulate import tabulate


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

    def __add__(self, other):
        pass

    def __mul__(self, other):
        pass


class RVFactory:
    @staticmethod
    def range(probability, start, stop, step=1):
        return RandomValue([(i, probability)for i in range(start, stop, step)])

    @staticmethod
    def evenly_range(start, stop, step=1):
        return RVFactory.range(1/(stop - start), start, stop, step)

    @staticmethod
    def arrange(values, probabilities):
        return RandomValue([(x, p) for (x, p) in zip(values, probabilities)])


def main():
    rv = RVFactory.evenly_range(1, 7)
    print(rv.__repr__())
    print(rv.__str__())


if __name__ == '__main__':
    main()



# def plusi(a, b):
#     from itertools import groupby
#     from operator import itemgetter
#     my_list = []
#     first = itemgetter(0)
#     for ax, ap in a:
#         for bx, bp in b:
#             my_list.append((ax+bx, ap*bp))
#     sums = [(k, sum(item[1] for item in tups_to_sum))
#             for k, tups_to_sum in
#             groupby(sorted(my_list, key=first), key=first)]
#     return sums


# def multi(a, b):
#     from itertools import groupby
#     from operator import itemgetter
#     my_list = []
#     first = itemgetter(0)
#     for ax, ap in a:
#         for bx, bp in b:
#             my_list.append((ax*bx, ap*bp))
#     sums = [(k, sum(item[1] for item in tups_to_sum))
#             for k, tups_to_sum in
#             groupby(sorted(my_list, key=first), key=first)]
#     return sums