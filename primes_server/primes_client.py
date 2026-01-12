import asyncio
import time

n = 0

async def prime_client(number, client_id):
    while True:
        #print(f"Echo client {client_id}")
        reader, writer = await asyncio.open_connection("", 25000)
        #print(f"{client_id} connected")
        writer.write(f'{number}'.encode('utf-8'))
        await writer.drain()
        resp = await reader.read(10000)
        #print(f"{client_id} got: " + str(resp))
        global n
        n += 1

async def monitor():
    while True:
        global n
        await asyncio.sleep(1)
        print(f"Conn/s {n}")
        n = 0

async def main():
    n = [1000, 2000, 3000, 4000]
    tasks = []
    for i in n:
        tasks.append(asyncio.create_task(prime_client(i, "n")))
    tasks.append(asyncio.create_task(monitor()))
    await asyncio.gather(*tasks)

asyncio.run(main())
