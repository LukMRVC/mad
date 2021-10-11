from typing import List
import math
from normal_distribution import normal_distribution
import matplotlib.pyplot as plt
import numpy as np
from interval import Interval


class IrisMatrix:
    def __init__(self, dataset: List[List[float]]):
        self.cols: int = len(dataset[0])
        self.rows: int = len(dataset)
        self.m: List[List[float]] = dataset

    def calc_avg_on_col(self, col_idx: int) -> float:
        return sum(map(lambda r: r[col_idx], self.m)) / self.rows

    def calc_variance_on_col(self, col_idx: int, avg: float) -> float:
        col = map(lambda r: r[col_idx], self.m)
        total = 0
        for n in col:
            total += (n - avg) * (n - avg)

        return total / self.rows

    def calc_total_var(self, total_avg: List[float]) -> float:
        total = 0
        for row in self.m:
            distance = euclid_distance(total_avg, row)
            total += distance * distance

        return total / self.rows

    def get_col_vector(self, col_idx: int) -> List[float]:
        return list(map(lambda r: r[col_idx], self.m))


def euclid_distance(avg_vec: List[float], vec: List[float]):
    distance = 0
    for i in range(len(avg_vec)):
        point_distance = math.sqrt(
            (avg_vec[i] - vec[i]) * (avg_vec[i] - vec[i]))
        distance += point_distance
    return distance


def load_iris_dataset(file_name: str):
    dataset = []
    with open(file_name) as f:
        header = f.readline()
        for line in f:
            dataset.append([
                float(x.replace(',', '.'))
                for x in line.split(';')[:-1]
            ])
    return dataset


if __name__ == '__main__':
    iris = load_iris_dataset('iris.csv')
    iris_matrix = IrisMatrix(iris)
    avgs = []
    variances = []
    for _ in range(iris_matrix.cols):
        avgs.insert(_, iris_matrix.calc_avg_on_col(_))
        variances.insert(_, iris_matrix.calc_variance_on_col(_, avgs[_]))

    print(f'Column averages: {avgs}')
    print(f'Column variances: {variances}')

    total_var = iris_matrix.calc_total_var(avgs)

    print(f'Total Variance: {total_var}')

    sepal_lengths = iris_matrix.get_col_vector(0)

    interval_len = 0.25
    min_len = min(sepal_lengths)
    max_len = max(sepal_lengths)
    curr_max = min_len + interval_len
    intervals = [Interval(min_len, curr_max)]
    while curr_max < max_len:
        intervals.append(Interval(curr_max, curr_max + interval_len))
        curr_max += interval_len

    for i in intervals:
        for l in sepal_lengths:
            if i.in_interval(l):
                i.increase()

    for i in intervals:
        i.set_probability(len(sepal_lengths))

    plt.ylabel('Empiric distributions')
    plt.xlabel('Intervals middle')
    plt.bar([i.end for i in intervals], [i.p for i in intervals])
    plt.show()

    i = 1
    teoretical_x = []
    teoretical_y = []
    while i <= 10:
        teoretical_x.append(i)
        teoretical_y.append(normal_distribution(i, avgs[0], variances[0]))
        i += 0.1

    plt.ylabel('Teoretical distributions')
    plt.xlabel('teoretical random vars')
    plt.plot(teoretical_x, teoretical_y)
    plt.show()


    cumulative_normal_dist_empiric = []
    for i, _int in enumerate(intervals):
        cumulative_normal_dist_empiric.append(_int.p + sum([_i.p for _i in intervals[:i] ]))

    plt.ylabel("Cumulative empiric distributions")
    plt.xlabel("Intervals middle")
    plt.plot([i.end for i in intervals], cumulative_normal_dist_empiric)

    cumulative_normal_dist_teoretical = []
    for i, val in enumerate(teoretical_y):
        cumulative_normal_dist_teoretical.append( val + sum(teoretical_y[:i]))

    
    plt.ylabel("Cumulative teoretical normal distributions")
    plt.xlabel("teoretical random vars")
    plt.plot([i.end for i in intervals], cumulative_normal_dist_empiric)