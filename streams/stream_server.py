import asyncio

from fastapi import FastAPI, Request, Query
from fastapi.responses import StreamingResponse

import json
import logging
import random

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Streaming Server")

async def fake_data_creator():
    for i in range(1, 10):
        yield (f"Generated some data {i}\n")
        await asyncio.sleep(1)

async def coordinate_generator():
    for i in range(10):
        data = {
            "id": i,
            "x" : i * 10,
            "y" : random.randint(0, 100)
        }
        json_str = json.dumps(data)
        yield f"{json_str}\n"
        await asyncio.sleep(0.1)

async def coordinate_generator_resume(request, last_id):
    current_id = last_id
    while current_id <= 1000:
        if await request.is_disconnected():
            logger.info("Client disconnected")
            break
        data = {
            "id": current_id,
            "x" : current_id * 10,
            "y" : random.randint(0, 100)
        }
        json_str = json.dumps(data)
        yield f"{json_str}\n"
        current_id += 1
        await asyncio.sleep(0.1)

@app.get("/stream")
async def stream():
    return StreamingResponse(fake_data_creator(), media_type = "text/plain")

@app.get("/stream-coords")
async def stream_coords():
    return StreamingResponse(coordinate_generator(), media_type = "application/x-ndjson")

@app.get("/stream-resume")
async def stream_coords(request: Request,
                        last_id: int = Query(0, description="The last id received by client")):
    return StreamingResponse(coordinate_generator_resume(request, last_id), media_type = "application/x-ndjson")



## Start server:
# uv run uvicorn stream_server:app --reload
# http://127.0.0.1:8000/docs