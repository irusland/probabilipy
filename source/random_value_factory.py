from fractions import Fraction

from source import random_value


class RVFactory:
    RV_NAME = 'Random Value from factory'

    def __init__(self, name):
        RVFactory.RV_NAME = name

    @staticmethod
    def range(probability, start, stop, step=1):
        return random_value.RandomValue(
            [(i, probability) for i in range(start, stop, step)],
            name=RVFactory.RV_NAME
        )

    @staticmethod
    def evenly_range(start, stop, step=1):
        return RVFactory.range(1 / (stop - start), start, stop, step)

    @staticmethod
    def arrange(values: list, probabilities: list):
        assert len(values) == len(probabilities)
        return random_value.RandomValue(
            [(x, p) for (x, p) in zip(values, probabilities)],
            name=RVFactory.RV_NAME
        )

    @staticmethod
    def fracrange(values: list, probabilities: list):
        pairs = []
        i = 0
        while i < len(values) * 2:
            p = 0
            p1 = probabilities[i]
            if p1 is float:
                if p1 // 1 == p1:
                    p = Fraction(p1, 1)
                else:
                    p = p1
                i += 1
            else:
                p2 = probabilities[i+1]
                p = Fraction(p1, p2)
                i += 2
            pairs.append((values[i//2 - 1], p))

        return random_value.RandomValue(
            pairs,
            name=RVFactory.RV_NAME
        )