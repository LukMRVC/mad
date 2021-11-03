from __future__ import annotations
from iris_data_matrix import load_iris_dataset
from karate_club import Matrix
from enum import Enum


class ClusterDistance(Enum):
    SINGLE_LINK = 0
    COMPLETE_LINK = 1
    AVERAGE_LINK = 2


def euclid_distance(a: iter, b: iter) -> float:
    distance = 0
    for idx in range(len(a)):
        point_distance = (a[idx] - b[idx]) * (a[idx] - b[idx])
        distance += point_distance
    return distance


class Cluster:
    def __init__(self, id: int, members: list):
        self.id = id
        self._members = members.copy()
        self.history = [id]

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f'Cluster ID {self.id} of {len(self._members)}: {str(tuple(self._members))}'

    def __eq__(self, other):
        if isinstance(other, Cluster):
            return self._members == other.members

    @property
    def members(self) -> list:
        return self._members

    def append(self, cluster: Cluster):
        self.history.extend(cluster.history)
        self._members.extend(cluster.members)

    def calc_distance(self, cluster: Cluster, distance_calc_method: ClusterDistance) -> float:
        distances = []
        for m in self._members:
            distances.extend(cluster._distance_from(m))

        if distance_calc_method == ClusterDistance.SINGLE_LINK:
            return min(distances)
        else:
            raise RuntimeError("Distance calc method not implemented")

    def _distance_from(self, vector) -> list:
        distances = []
        for m in self._members:
            distances.append(round(euclid_distance(vector, m), 3))
        return distances


class DistanceMatrix():
    def __init__(self, size: int, init_with: int = 0):
        self.size = size
        self.m = [init_with] * (self.size * self.size)

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        str_rep = ''
        for row in self.rows_i():
            str_rep += f'{row}\n'
        return str_rep

    def at(self, row, col):
        return self.m[row * self.size + col]

    def insert_at(self, row, col, val) -> None:
        self.m[row * self.size + col] = val
        self.m[col * self.size + row] = val

    def remove(self, row_col_idx):
        removed = 0
        for i in range(self.size):
            to_remove = (i * self.size) + row_col_idx - removed
            self.m.pop(to_remove)
            removed += 1
        b = self.m[:row_col_idx * (self.size - 1)]
        a = self.m[(row_col_idx + 1) * (self.size - 1):]
        b.extend(a)
        self.m = b.copy()
        self.size -= 1
        pass

    def rows_i(self):
        for i in range(0, len(self.m), self.size):
            yield self.m[i: i + self.size]


if __name__ == '__main__':
    iris_data = load_iris_dataset('iris.csv')
    clusters = [Cluster(i, [x]) for i, x in enumerate(iris_data[:10])]
    dst_matrix = DistanceMatrix(size=len(clusters), init_with=-1)
    inserts = False
    for row, c1 in enumerate(clusters):
        for col, c2 in enumerate(clusters):
            # already calculated
            if dst_matrix.at(row, col) > -1:
                continue
            # zero the diagonal
            if c2 == c1:
                dst_matrix.insert_at(row, col, 0)
            else:
                dst_matrix.insert_at(row, col, c1.calc_distance(c2, ClusterDistance.SINGLE_LINK))
                inserts = True

        if not inserts:
            print(f'No inserts for {row}')

    while dst_matrix.size > 1:
        minimal_cluster_distance = min(filter(lambda x: x != 0, dst_matrix.m))
        minimal_cluster_distance_idx = dst_matrix.m.index(minimal_cluster_distance)
        minimal_cluster_distance_row = minimal_cluster_distance_idx // dst_matrix.size
        minimal_cluster_distance_col = minimal_cluster_distance_idx - (minimal_cluster_distance_row * dst_matrix.size)
        print(f'MIN DISTANCE: {minimal_cluster_distance}, ROW: {minimal_cluster_distance_row}, COL: {minimal_cluster_distance_col}')
        print(dst_matrix)
        # I have indices of clusters that I need to merge

        try:
            c1 = clusters[minimal_cluster_distance_row]
            c2 = clusters[minimal_cluster_distance_col]
        except IndexError as ex:
            raise
        c1.append(c2)
        clusters.pop(minimal_cluster_distance_col)
        dst_matrix.remove(minimal_cluster_distance_col)

        for col, cluster in enumerate(clusters):
            if cluster == c1:
                dst_matrix.insert_at(minimal_cluster_distance_row, col, 0)
            else:
                dst_matrix.insert_at(minimal_cluster_distance_row, col,
                                     c1.calc_distance(cluster, ClusterDistance.SINGLE_LINK))
    print(dst_matrix.m)
    pass
    # matrix = DistanceMatrix(size=4, init_with=0)
    #
    # matrix.insert_at(0, 0, 1)
    # matrix.insert_at(0, 1, 2)
    # matrix.insert_at(0, 2, 3)
    # matrix.insert_at(0, 3, 4)
    #
    # matrix.insert_at(1, 2, 5)
    # matrix.insert_at(2, 3, 6)
    #
    # for row in matrix.rows_i():
    #     print(row)
    # print('----------------------------------------')
    #
    # matrix.remove(0)
    # for row in matrix.rows_i():
    #     print(row)
    # print('----------------------------------------')
    # matrix.remove_row(0)
    # for row in matrix.rows_i():
    #     print(row)
    # print('----------------------------------------')
    pass
