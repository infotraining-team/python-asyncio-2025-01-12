import asyncio

async def producer(q):
    print("Creating resources")
    await asyncio.sleep(2)
    print("Starting producer")
    for i in range(10):
        await q.put(f"task {i}")
        await asyncio.sleep(0.2)
    #await q.put(None)


async def consumer(q, name):
    print(f"Consumer {name} is starting")
    while True:
        task = await q.get()
        if task is None:
            print(f"Consumer {name} is finishing")
            await q.put(None)
            return
        print(f"{name} got {task}")
        await asyncio.sleep(0.5)


async def main():
    q = asyncio.Queue()
    p = asyncio.create_task(producer(q))
    cons = asyncio.gather(*[consumer(q, f"cons {i}") for i in range(3)])
    await p
    await q.put(None)
    await cons

asyncio.run(main())