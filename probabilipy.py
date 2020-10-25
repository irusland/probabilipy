from source.calculations import (
    dispersion as D,
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

    # ksi_1 = RVFactory('ξ').fractrange(
    #     [-1,    0,      1],
    #     [1,6,   1,3,    1,2]
    # )

    ksi_1 = RVFactory('ξ').fractrange(
        [-2,    -1,     1,      2],
        [1,4,   1,4,    1,4,    1,4]
    )

    ksi_2 = ksi_1 ** 2
    ksi_3 = ksi_1 ** 3
    ksi_4 = ksi_1 ** 4

    print(ksi_1, ksi_2, ksi_3, ksi_4)
    print('E(ksi_1)', E(ksi_1))
    print('E(ksi_2)', E(ksi_2))
    print('E(ksi_3)', E(ksi_3))
    print('E(ksi_4)', E(ksi_4))
    print('Cov(ksi_1, ksi_2)', Cov(ksi_1, ksi_2))
    print('D(ksi_1)', D(ksi_1))
    print('D(ksi_2)', D(ksi_2))

    # ksi = RVFactory('ξ').evenly_range(1, 7)
    # mu = RVFactory('μ').fractrange(
    #     [0,     1],
    #     [1,4,   3,4],
    # )
    # theta = ksi ** 2
    # print(ksi, mu, theta)
    # print(float(E(theta)))


if __name__ == '__main__':
    main()
