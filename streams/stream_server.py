import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

import json
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Streaming Server")

async def fake_data_creator():
    for i in range(1, 10):
        yield (f"Generated some data {i}\n")
        await asyncio.sleep(1)

@app.get("/stream")
async def stream():
    return StreamingResponse(fake_data_creator(), media_type = "text/plain")