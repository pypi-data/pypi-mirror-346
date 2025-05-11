import numpy as np

class Real:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def sample(self, n=1):
        return np.random.uniform(self.low, self.high, size=n)

    def transform(self, value):
        return (value - self.low) / (self.high - self.low)

    def inverse_transform(self, value):
        return value * (self.high - self.low) + self.low


class Integer:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def sample(self, n=1):
        return np.random.randint(self.low, self.high + 1, size=n)

    def transform(self, value):
        return (value - self.low) / (self.high - self.low)

    def inverse_transform(self, value):
        return int(round(value * (self.high - self.low) + self.low))


class Categorical:
    def __init__(self, choices):
        self.choices = choices

    def sample(self, n=1):
        return [np.random.choice(self.choices) for _ in range(n)]

    def transform(self, value):
        return self.choices.index(value) / (len(self.choices) - 1)

    def inverse_transform(self, value):
        idx = round(value * (len(self.choices) - 1))
        return self.choices[int(idx)]