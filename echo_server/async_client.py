import asyncio
import time

async def echo_client(delay, client_id):
    print(f"Echo client {client_id}")
    reader, writer = await asyncio.open_connection("", 25000)
    print(f"{client_id} connected")

    while True:
        writer.write(f'Hello from client {client_id}'.encode('utf-8'))
        await writer.drain()
        resp = await reader.read(1000)
        print(f"{client_id} got: " + str(resp))
        time.sleep(delay)

asyncio.run(echo_client(1, "Leszek"))