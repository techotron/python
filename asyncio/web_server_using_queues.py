import asyncio
import logging
import base64
import json

from aiohttp_healthcheck import HealthCheck
from aiohttp import web

# Need to define the queue in a scope where the handler can access it. This may not be the best place but fine for this example
queue: asyncio.Queue = asyncio.Queue()
concurrency = 2
batch_size = 5

async def http_handler(request):
    body = await request.read()

    # When a request comes in, just put the body in the queue and respond to the client some success message
    await queue.put(body)

    resp = json.dumps({"Success": True})
    return web.Response(text=resp, content_type="application/json")

async def init_app():
    logger = logging.getLogger("aiohttp.server")
    health = HealthCheck()
    app = web.Application(client_max_size=1024**4)
    logging.basicConfig(handlers=logger.handlers, level=logger.level)
    app.router.add_get("/health", health)
    app.router.add_post("/v1/path1", http_handler)
    app.router.add_post("/v1/path2", http_handler)

    # Get the running loop and create tasks (in this case, queue consumers) to it
    loop = asyncio.get_running_loop()
    [loop.create_task(kinesis_batch_executor(name=i)) for i in range(concurrency)]

    return app

async def kinesis_batch_executor(name):
    batch_messages = []
    logging.info(f"[worker{name}] starting kinesis_batch_executor")
    while True:
        body = await queue.get()
        payload = base64.b64encode(body).decode()
        data = json.dumps(
            {"payload": payload}
        )
        batch_messages.append(data)

        # When we have enough message to batch put to kinesis, call the API
        if len(batch_messages) == batch_size:
            logging.info(f"[worker{name}] Length of batch is {len(batch_messages)}")

            # Mimic IO when doing a batch API call to kinesis
            await asyncio.sleep(1)

            # Empty this instance of batch_messages once they've been processed
            batch_messages.clear()

        queue.task_done()

if __name__ == "__main__":
    app = init_app()
    web.run_app(app)
