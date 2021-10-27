from karate_club import Matrix

def process():
    with open('./KarateClub.csv') as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    nodes = set()
    for l in data:
        n, m = l.split(';')
        nodes.add(int(n))
        nodes.add(int(m))

    n: int = len(nodes)
    paths = Matrix(n, n, init_with=999999)
    for l in data:
        r, c = l.split(';')
        paths.insert_at(int(r), int(c), 1)
        paths.insert_at(int(c), int(r), 1)

    for i in range(1, n + 1):
        paths.insert_at(i, i, 0)

    # print('---------------------------------------------------------------------------------'
    #       '-----------------------------------------')

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                if paths.at(j, i) + paths.at(i, k) < paths.at(j, k):
                    paths.insert_at(j, k, paths.at(j, i) + paths.at(i, k))
                pass
            pass
        pass
    pass

    for row in paths.rows_i():
        print(row)

    vertex_mean = []
    vertex_closeness_centralities = []
    for v, row in enumerate(paths.rows_i()):
        vertex_mean.append(round(sum(row) / len(nodes), 6))
        vertex_closeness_centralities.append(round(1 / vertex_mean[-1], 6))

    global_max = 0
    global_graph_avg = 0

    for row in paths.rows_i():
        global_max = max(global_max, max(row))
        global_graph_avg += sum(row)

    global_graph_avg = 2 * global_graph_avg / (n * (n - 1))
    print(f'\n')
    print(f'Graph avg is: {global_max}')
    print(f'Global mean distance is: {global_graph_avg}')

    print('Vertices mean distances:')
    for i, mean in enumerate(vertex_mean):
        print(f'V{i + 1}: {mean}')
    print('Vertices closeness centralities:')
    for i, centrility in enumerate(vertex_closeness_centralities):
        print(f'V{i + 1}: {centrility:>0.6f}')


if __name__ == '__main__':
    process()
