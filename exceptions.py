import asyncio

async def coro(delay, crash):
    print(f"Starting coro with delay {delay}")
    await asyncio.sleep(delay)
    if crash:
        raise ValueError
    else:
        return 42

async def main():
    c1 = coro(1, True)
    try:
        res = await c1
        print(res)
    except ValueError:
        print("got error")

async def main_gather():
    tasks = [coro(2, False), coro(3, True)]
    try:
        res = await asyncio.gather(*tasks)
        print(res)
    except ValueError:
        print("Crash!!")

async def main_gather_exceptions():
    tasks = [coro(2, False), coro(3, True)]
    try:
        res = await asyncio.gather(*tasks, return_exceptions=True)
        print(res)
    except ValueError:
        print("Crash!!")

asyncio.run(main_gather_exceptions())