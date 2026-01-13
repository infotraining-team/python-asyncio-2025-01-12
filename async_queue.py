import asyncio

async def producer(q):
    print("Creating resources")
    await asyncio.sleep(2)
    print("Starting producer")
    for i in range(10):
        await q.put(f"task {i}")
        await asyncio.sleep(0.1)
    print("Producer finished")

async def consumer(q, name):
    print(f"Consumer {name} is starting")
    while True:
        task = await q.get()
        print(f"{name} got {task}")
        await asyncio.sleep(0.5)
        q.task_done()

async def main():
    q = asyncio.Queue()
    p = asyncio.create_task(producer(q))
    cons = asyncio.gather(*[consumer(q, f"cons {i}") for i in range(3)])
    await p
    await q.join() # q is empty and all consumers finished task processing (called task_done())
    cons.cancel()
    try:
        await cons
    except asyncio.CancelledError:
        pass


async def main_simple():
    q = asyncio.Queue()
    await q.put(1)
    await q.put(2)
    for i in range(2):
        res = await q.get()
        print(res)

asyncio.run(main())