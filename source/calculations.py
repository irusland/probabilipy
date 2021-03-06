from fractions import Fraction

from source import random_value as rv

DEBUG = False


def _pair_product(pair):
    if DEBUG:
        print(pair)
    x, p = pair
    return x * p


def expected_value(random_value: 'rv.RandomValue'):
    """Мат ожидание"""
    return sum(map(_pair_product, random_value.probability_pairs))


def dispersion(random_value: 'rv.RandomValue'):
    """Дисперсия"""
    return expected_value((random_value - expected_value(random_value)) ** 2)


def covariance(
        a: 'rv.RandomValue',
        b: 'rv.RandomValue'):
    """Коваривация"""
    return expected_value(a * b) - expected_value(a) * expected_value(b)


def correlation(a: 'rv.RandomValue', b: 'rv.RandomValue'):
    """Коврреляция"""
    return (covariance(a, b)
            / (pow(dispersion(a), 1 / 2)
               * pow(dispersion(b), 1 / 2)))


def arrange_function(a: 'rv.RandomValue'):
    # todo
    raise NotImplementedError()


def quantile(a: 'rv.RandomValue', q):
    # todo
    raise NotImplementedError()


def median(a: 'rv.RandomValue'):
    # todo
    return quantile(a, Fraction(1, 2))

