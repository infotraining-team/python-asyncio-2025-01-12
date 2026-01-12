import asyncio

async def coro(delay, crash=False):
    print(f"Starting coro with delay {delay}")
    await asyncio.sleep(delay)
    if crash:
        raise ValueError
    else:
        return 42

async def waiting():
    try:
        res = await asyncio.wait_for(coro(3), 1)
        print(res)
    except TimeoutError:
        print("Timeout")

async def waiting_for_first():
    coros = [coro(5), coro(2), coro(1)]
    tasks = [asyncio.create_task(c) for c in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for c in done:
        res = await c
        print(res)

async def waiting_for_first_exc():
    coros = [coro(5), coro(2), coro(1, True)]
    tasks = [asyncio.create_task(c) for c in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for c in done:
        try:
            res = await c
        except ValueError:
            print("Error")
    print("wait for pending")
    for c in pending:
        res = await c
        print(f"got {res}")

asyncio.run(waiting_for_first_exc())