import { Application, Router } from "https://deno.land/x/oak/mod.ts";
import BarabasiAlbert from './barabasiAlberts.ts';

const router = new Router();

router
    .get('/ba', (context) => {
        const params = context.request.url.searchParams;
        const startNodes = parseInt(params.get('nodes') || '', 10);
        const steps = parseInt(params.get('steps') || '', 10);
        const connectionParam = parseInt(params.get('connection') || '', 10);

        try {
            context.response.headers.set('Content-Type', 'json');
            context.response.body = BarabasiAlbert(startNodes, steps, connectionParam);
        } catch (error) {
            context.response.status = 400;
            context.response.body = error.message;
        }
    });

const app = new Application();
app.use(router.routes());
app.use(router.allowedMethods());

console.log('http://localhost:8000');
await app.listen({ port: 8000 });
