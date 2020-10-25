from source.random_value_factory import RVFactory


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
        [1 / 3, 1 / 3, 1 / 3],
    )
    print(ksi)
    print(ksi * ksi)
    print(ksi * ksi * ksi)
    print(ksi * ksi * ksi * ksi)


if __name__ == '__main__':
    main()
