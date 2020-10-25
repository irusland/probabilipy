from source import random_value


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
    def __init__(self, this: 'random_value.RandomValue', other, operation):
        self.message = (
            f'Cannot apply {operation} between\n'
            f'\t{this} of type {type(this)} and\n'
            f'\t{other} of type {type(other)}'
        )
        super().__init__(self.message)


class RandomValueCastError(Exception):
    def __init__(self, other):
        self.message = (
            f'Cannot cast {other} of type {type(other)} to '
            f'{type(random_value.RandomValue)}'
        )
        super().__init__(self.message)
