"""
Stahnout Gephi a vizualizovat
"""
import matplotlib.pyplot as plt


class Matrix:

    def __init__(self, rows, cols, init_with=0) -> None:
        self.rows = rows
        self.cols = cols
        self.m = [init_with] * (rows * cols)

    def insert_at(self, row, col, val) -> None:
        self.m[(row - 1) * self.cols + (col - 1)] = val

    def at(self, row, col) -> int:
        return self.m[(row - 1) * self.cols + (col - 1)]

    def rows_i(self):
        for i in range(0, len(self.m), self.cols):
            yield self.m[i: i + self.cols]

    def rows_after(self, i):
        for j in range(self.cols * i):
            yield self.m[j: j + self.cols]

    def get_row(self, r: int):
        return self.m[(r - 1) * self.cols: r * self.cols]


def karate():
    with open('./KarateClub.csv') as f:
        data = f.readlines()

    data = [x.strip() for x in data]
    nodes = set()
    for l in data:
        n, m = l.split(';')
        nodes.add(int(n))
        nodes.add(int(m))

    m = Matrix(len(nodes), len(nodes))
    for l in data:
        r, c = l.split(';')
        m.insert_at(int(r), int(c), 1)
        m.insert_at(int(c), int(r), 1)

    _min = 9999
    _max = 0
    nodes_degrees = []
    for r in m.rows_i():
        degree = sum(r)
        _min = min(degree, _min)
        _max = max(degree, _max)
        nodes_degrees.append(degree)

    avg_degree = round(sum(nodes_degrees) / len(nodes), 2)
    print('Min degree: ', _min)
    print('Max degree: ', _max)
    print('Avg degree: ', avg_degree)

    node_degree_freq = []
    for i in nodes_degrees:
        node_degree_freq.append(nodes_degrees.count(i))

    plt.ylabel('# number nodes')
    plt.xlabel('degrees')
    f1 = plt.figure(1)
    plt.bar(nodes_degrees, node_degree_freq)

    plt.ylabel('relative # number nodes')
    plt.xlabel('degrees')
    f2 = plt.figure(2)
    plt.bar(nodes_degrees, [x / len(nodes) for x in node_degree_freq])
    # plt.show()
    pass

    adjacency_list = {}
    for n in nodes:
        adjacency_list[n] = [int(x.split(';')[1])
                             for x in data if int(x.split(';')[0]) == n]
        adjacency_list[n].extend([int(x.split(';')[0])
                                  for x in data if int(x.split(';')[1]) == n])
    print(adjacency_list)

    _min = 9999
    _max = 0
    vertex_degrees = []
    for v, edges in adjacency_list.items():
        degree = len(edges)
        _min = min(degree, _min)
        _max = max(degree, _max)
        vertex_degrees.append(degree)

    avg_vertex = round(sum(vertex_degrees) / len(nodes), 2)
    print('Min vertex degree: ', _min)
    print('Max vertex degree: ', _max)
    print('Avg vertex degree: ', avg_vertex)

    vertex_degree_freq = []
    for i in vertex_degrees:
        vertex_degree_freq.append(vertex_degrees.count(i))

    plt.ylabel('# number verticis')
    plt.xlabel('degrees')
    f3 = plt.figure(3)
    plt.bar(vertex_degrees, vertex_degree_freq)

    plt.ylabel('relative # number verticies')
    plt.xlabel('degrees')
    f4 = plt.figure(4)
    plt.bar(vertex_degrees, [x / len(nodes) for x in vertex_degree_freq])
    plt.show()


if __name__ == '__main__':
    karate()
