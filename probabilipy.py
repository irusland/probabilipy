from source.calculations import (
    statistical_dispersion as D,
    expected_value as E,
    covariance as Cov,
    correlation as r,
)
from source.random_value_factory import RVFactory


def main():
    # ksi = RVFactory('ξ').arrange(
    #     [-1,    0,      1],
    #     [1/3,   1/3,    1/3]
    # )
    # ksi_2 = ksi ** 2
    # print(ksi)
    # print(ksi_2)
    # print(r(ksi, ksi_2))

    ksi = RVFactory('ξ').fracrange(
        [-1,    0,      1],
        [1,6,   1,3,    1,2]
    )
    ksi_2 = ksi ** 2

    print(ksi)
    print(ksi_2)
    print(E(ksi))
    print(E(ksi_2))
    print(Cov(ksi, ksi_2))


if __name__ == '__main__':
    main()
