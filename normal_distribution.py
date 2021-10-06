from typing import List
import math


def get_exp(x: float, mean: float, variance: float) -> float:
    numerator = (x - mean) * (x - mean)
    denominator = 2 * variance
    return math.exp(-(numerator / denominator))


def normal_distribution(x: float, mean: float, var: float) -> float:
    first = 1 / (math.sqrt(2 * math.pi * var))
    second = get_exp(x, mean, var)
    return first * second
    pass
