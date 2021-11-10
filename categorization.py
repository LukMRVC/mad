

from functools import reduce


class DataSet:

    def __init__(self, csv_lines, has_header=True) -> None:
        if has_header:
            self.data = [line.split(';') for line in csv_lines[1:]]
            self.header = csv_lines[0].split(';')
        self.cls_col_idx = len(self.header) - 1

    def __repr__(self) -> str:
        s = str(self.header) + '\n'
        for row in self.data:
            s += f'{row}\n'
        return s

    def __str__(self) -> str:
        return self.__repr__()

    def column(self, col_idx: int) -> list:
        return [x[col_idx] for x in self.data]

    def row(self, row_idx: int) -> list:
        return self.data[row_idx]

    def rows(self) -> list:
        return self.data


class CountingSet:
    def __init__(self, dataset: list) -> None:
        self.dataset = dataset
        self.s = set(dataset)
        self.occurences = {}
        self.probabilities = {}
        self.total = len(dataset)
        self.count_in_set()

    def __repr__(self) -> str:
        return str(self.occurences)

    def __str__(self) -> str:
        return self.__repr__()

    def items(self):
        return self.probabilities.items()

    def count_in_set(self) -> None:
        for d in self.s:
            self.occurences[d] = self.dataset.count(d)
            self.probabilities[d] = self.occurences[d] / self.total

    def recalc(self) -> None:
        self.count_in_set()

    def probabilty(self, of: str) -> float:
        if of not in self.occurences:
            raise KeyError(f"{of} not in couting set")
        return self.occurences[of] / self.total


def load_weather_set():
    with open('weather.csv') as f:
        lines = [l.strip() for l in f.readlines()]
        return DataSet(lines)
    pass


def get_2d_col(data: list, col_idx: int) -> list:
    return [x[col_idx] for x in data]


def naive_bayers_prob(set_list: list, idx: int, current_keys='', product_list=[]) -> None:
    if idx < len(set_list) - 1:
        for key, values in set_list[idx].items():
            naive_bayers_prob(set_list, idx + 1,
                              f'{current_keys} {key} ({values:.2f}) x', [*product_list, values])
    else:
        print(
            f'{current_keys.rstrip("x")} = {reduce((lambda x, y: x * y), product_list):.6f}')


if __name__ == '__main__':
    weather_set = load_weather_set()
    cls_col = weather_set.cls_col_idx
    classes = set(weather_set.column(cls_col))
    rows = weather_set.rows()

    cls_counters = {}
    prior_values = CountingSet(weather_set.column(cls_col))
    for cls in classes:
        r = [x for x in rows if x[cls_col] == cls]
        cls_counters[cls] = []
        for i in range(cls_col):
            cls_counters[cls].append(CountingSet(get_2d_col(r, i)))
        cls_counters[cls].append(prior_values)

    for key, values in cls_counters.items():
        # print(f'class = {key}')
        naive_bayers_prob(values, 0, f'class = {key}: ')
