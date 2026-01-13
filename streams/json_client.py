import asyncio
import httpx
import json

async def consume_stream():
    url = "http://127.0.0.1:8000/stream-coords"
    print("Connecting")
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            print("Connection established")
            async for chunk in response.aiter_text():
                try:
                    data = json.loads(chunk)
                    print(f"Got point {data['id']}, x: {data['x']}, y: {data['y']}")
                except json.JSONDecodeError:
                    print("Failed to parse line")

asyncio.run(consume_stream())