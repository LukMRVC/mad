from typing import List
from math import sqrt


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


def euclid_distance(avg_vec: List[float], vec: List[float]):
    distance = 0
    for i in range(len(avg_vec)):
        point_distance = sqrt((avg_vec[i] - vec[i]) * (avg_vec[i] - vec[i]))
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
