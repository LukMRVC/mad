
type Pair = [number, number];
type Graph = { edges: Array<Pair>, vertices: number[] }
// N - number of starting nodes, S - number of steps, C - new connections
export default function barabasiAlbert(n: number, s: number, c: number): Graph {
    if (c < 1 || c > n) {
        throw new Error('Connection param of nodes must be between 1 and N');
    }

    // get starting vertices
    const vertices = [];
    for (let i = 1; i < n + 1; ++i) {
        vertices.push(i);
    }

    const edges: Pair[] = [];
    // let D(n) be the degree of vertex N, then this array contais number
    // representing vertex N D(n) times
    const vertexDegreeExploded = [];
    for (const v of vertices) {
        // connect each vertex with C edges
        while (vertexDegreeExploded.filter((vertex) => vertex === v).length < c) {
            let other = v;
            while (other === v) {
                other = pick(vertices);
            }
            vertexDegreeExploded.push(v, other);
            edges.push([v, other]);
        }
    }

    for (let i = 0; i < s; ++i) {
        const nextVertex = n + i + 1;
        const connected: number[] = [];
        for (let j = 0; j < c; ++j) {
            let other = null;
            while (other === null || connected.includes(other)) {
                other = pick(vertexDegreeExploded);
            }
            connected.push(other);
            edges.push([nextVertex, other]);
        }

        // degree of some vertices increased, so they must be included here
        vertexDegreeExploded.push(...connected);
        // push this next vertex C times
        for (let j = 0; j < c; ++j) {
            vertexDegreeExploded.push(nextVertex);
        }
        // add the vertex to the vertices array
        vertices.push(nextVertex);
    }

    return {
        edges,
        vertices,
    };
}

function pick<T>(arr: T[]): T {
    return arr[arr.length * Math.random() | 0];
}