import asyncio
import httpx
import json

async def consume_stream():
    url = "http://127.0.0.1:8000/stream-resume"
    last_seen_id = 0
    while True:
        try:
            connect_url = f"{url}?last_id={last_seen_id}"
            print("Connecting")
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", connect_url) as response:
                    print("Connection established")
                    async for chunk in response.aiter_text():
                        try:
                            data = json.loads(chunk)
                            print(f"Got point {data['id']}, x: {data['x']}, y: {data['y']}")
                            last_seen_id = data["id"]
                        except json.JSONDecodeError:
                            print("Failed to parse line")
        except Exception as e:
            print("Connection lost, retrying")
            await asyncio.sleep(3)

async def consume_stream_simple():
    url = "http://127.0.0.1:8000/stream"
    print("Connecting")
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            print("Connection established")
            async for chunk in response.aiter_text():
                print(f"Received {chunk.strip()}")

async def main():
    await asyncio.gather(consume_stream_simple(), consume_stream())

asyncio.run(main())