import { Application, Router } from "https://deno.land/x/oak/mod.ts";
import { oakCors } from "https://deno.land/x/cors/mod.ts";
import BarabasiAlbert from './barabasiAlberts.ts';
import {
    constructGraph,
    globalMeanRank,
    rankDistribution,
    rankVertices,
    graphToMatrix,
    graphDiameter,
    graphGlobalMeanDistance,
    closenessCentralitiesAndMeanDistances,
} from "./analytics.ts";

const router = new Router();

router
    .get('/ba', (context) => {
        const params = context.request.url.searchParams;
        const startNodes = parseInt(params.get('nodes') || '', 10);
        const steps = parseInt(params.get('steps') || '', 10);
        const connectionParam = parseInt(params.get('connection') || '', 10);
        const download = params.has('download');
    
        try {
            const graph = BarabasiAlbert(startNodes, steps, connectionParam);
            if (download) {
                const edges = graph.edges.map((pair) => `${pair[0]},${pair[1]}`).join('\n');
                const fileContent = 'source,target\n' + edges;
                context.response.headers.set('Content-Length', fileContent.length.toString());
                context.response.headers.set('Content-Disposition', 'attachment; filename=graph.csv');
                context.response.body = fileContent;
            } else {
                context.response.headers.set('Content-Type', 'application/json');
                context.response.body = graph;
            }
        } catch (error) {
            context.response.status = 400;
            context.response.body = error.message;
        }
    })
    .post('/analytics', async (ctx) => {
        const { request, response } = ctx;
        const body = request.body({ type: 'form-data' });
        const formData = await body.value.read();
        if (formData.files) {
            const text = Deno.readTextFileSync(formData.files[0].filename || '');
            if (text) {
                const graph = constructGraph(text);
                const ranks = rankVertices(graph);
                const globalRank = globalMeanRank(ranks);
                const distributionsOfRanks = rankDistribution(ranks);
                const graphMatrix = graphToMatrix(graph);
                const diameter = graphDiameter(graphMatrix);
                const centralities = closenessCentralitiesAndMeanDistances(graphMatrix);
                const globalMeanDistance = graphGlobalMeanDistance(graphMatrix);

                response.headers.append('Content-Type', 'application/json');
                response.body = JSON.stringify({
                    graph,
                    ranks,
                    globalRank,
                    distributionsOfRanks,
                    diameter, 
                    centralities,
                    globalMeanDistance,
                });
            }
        }
    });

const app = new Application();
app.use(oakCors());
app.use(router.routes());
app.use(router.allowedMethods());

console.log('http://localhost:8000');
await app.listen({ port: 8000 });
