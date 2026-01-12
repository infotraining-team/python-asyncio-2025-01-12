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
        await asyncio.sleep(delay)

async def main():
    c1 = echo_client(0.5, "Leszek")
    c2 = echo_client(0.2, "Robert")
    c3 = echo_client(0.1, "Bruno")
    print("Starting")
    await asyncio.sleep(1)
    res = await asyncio.gather(c1, c2, c3)

async def main_with_tasks():
    t1 = asyncio.create_task(echo_client(5, "Leszek"))
    t2 = asyncio.create_task(echo_client(2, "Robert"))
    t3 = asyncio.create_task(echo_client(3, "Bruno"))
    print("Starting")
    await asyncio.sleep(1)
    print("Gather")
    res = await asyncio.gather(t1, t2, t3)

asyncio.run(main_with_tasks(), debug=True)