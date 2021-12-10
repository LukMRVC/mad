import { Graph, Pair } from "./barabasiAlberts.ts";

// ranks - key is vertex, value is a degree
type ranks = { [key: number]: number };
export function rankVertices(graph: Graph): ranks {
  return graph.edges.reduce((acc: ranks, pair: Pair) => {
    const [first, second] = pair;

    if (!(first in acc)) {
      acc[first] = 0;
    }
    acc[first] += 1;

    if (!(second in acc)) {
      acc[second] = 0;
    }

    acc[second] += 1;

    return acc;
  }, {});
}

export function globalMeanRank(ranks: ranks): number {
  const rankSum = Object.values(ranks).reduce((acc, val) => acc + val, 0);
  return rankSum / (Object.keys(ranks)).length;
}

export function constructGraph(edgesStr: string): Graph {
  const edgePairs = edgesStr.split("\n");
  const edges: Pair[] = edgePairs.map((pair: string, idx) => {
    if (idx === 0) {
      return [0, 0];
    }
    const [first, second] = pair.split(",");
    return [parseInt(first), parseInt(second)];
  });
  edges.shift();

  const vertices = edges.reduce((acc, pair) => {
    const [f, s] = pair;
    acc.add(f);
    acc.add(s);
    return acc;
  }, new Set<number>());

  return {
    edges,
    vertices: Array.from<number>(vertices),
  };
}

/*
Calculates degree distribution - how many vertices with degree K are in network
this time the key is degree, and the value is number of vertices, that have given degree
*/
export function rankDistribution(ranks: ranks): ranks {
  const allDegrees = Object.values(ranks);
  const degrees = Array.from(new Set(allDegrees));
  const distribution: ranks = {};
  for (const kDegree of degrees) {
    distribution[kDegree] = allDegrees.filter((deg) => deg === kDegree).length;
  }
  return distribution;
}

export function graphToMatrix(graph: Graph): Matrix {
  const matrix = new Matrix(
    graph.vertices.length,
    graph.vertices.length,
    99999,
  );
  for (const edge of graph.edges) {
    const [first, second] = edge;
    matrix.insertAt(first, second, 1);
    matrix.insertAt(second, first, 1);
  }

  for (let i = 1; i < graph.vertices.length + 1; i++) {
    matrix.insertAt(i, i, 0);
  }

  for (let i = 1; i < graph.vertices.length + 1; ++i) {
    for (let j = 1; j < graph.vertices.length + 1; ++j) {
      for (let k = 1; k < graph.vertices.length + 1; ++k) {
        if (matrix.at(j, i) + matrix.at(i, k) < matrix.at(j, k)) {
          matrix.insertAt(j, k, matrix.at(j, i) + matrix.at(i, k));
        }
      }
    }
  }

  return matrix;
}

export function graphDiameter(graphMatrix: Matrix): number {
  let globalMax = 0;
  for (const row of graphMatrix.rowsIterator()) {
    globalMax = Math.max(globalMax, Math.max(...row));
  }
  return globalMax;
}

export function graphGlobalMeanDistance(graphMatrix: Matrix): number {
    let globalMeanDistance = 0;
    let rowIdx = 0;
    for (const row of graphMatrix.rowsIterator()) {
      globalMeanDistance += sum(row.slice(rowIdx));
      rowIdx++;
    }
    return 2 * globalMeanDistance / (graphMatrix.rows * (graphMatrix.rows - 1));
}

const sum = (arr: number[]) => arr.reduce((acc, curr) => acc + curr, 0);

type centralitiesAndMeanDistance = {
  centralities: ranks;
  meanDistances: ranks;
};
export function closenessCentralitiesAndMeanDistances(
  graphMatrix: Matrix,
): centralitiesAndMeanDistance {
  const centralities: ranks = {};
  const meanDistances: ranks = {};
  let vertexNumber = 0;
  for (const row of graphMatrix.rowsIterator()) {
    vertexNumber += 1;
    meanDistances[vertexNumber] = sum(row) / graphMatrix.rows;
    centralities[vertexNumber] = 1.0 / meanDistances[vertexNumber];
  }

  return {
    centralities,
    meanDistances,
  };
}

class Matrix {
  rows: number;
  cols: number;
  m: number[];

  constructor(rows: number, cols: number, initWith: number = 0) {
    this.rows = rows;
    this.cols = cols;
    this.m = Array.from({ length: (rows * cols) }, () => initWith);
  }

  insertAt(row: number, col: number, value: number): void {
    this.m[(row - 1) * this.cols + (col - 1)] = value;
  }

  at(row: number, col: number): number {
    return this.m[(row - 1) * this.cols + (col - 1)];
  }

  *rowsIterator() {
    for (let i = 0; i < this.m.length; i += this.cols) {
      yield this.m.slice(i, i + this.cols);
    }
  }
}
