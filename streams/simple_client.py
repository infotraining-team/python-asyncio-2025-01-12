import asyncio
import httpx

async def consume_stream():
    url = "http://127.0.0.1:8000/stream"
    print("Connecting")
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            print("Connection established")
            async for chunk in response.aiter_text():
                print(f"Received {chunk.strip()}")

asyncio.run(consume_stream())