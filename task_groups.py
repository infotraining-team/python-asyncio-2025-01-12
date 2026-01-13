import asyncio

async def worker(delay, error=False):
    await asyncio.sleep(delay)
    if error:
        raise ValueError("Error!!")
    return f"Done after {delay}"

async def main():
    print("Starting tasks")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(worker(3))
        t2 = tg.create_task(worker(2))
        #some unsafe code
    print("All taks finished")
    print(f"Results : {t1.result()}, {t2.result()}")

async def failing_main():
    print("Starting tasks")
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(worker(2))
            t2 = tg.create_task(worker(5))
            t3 = tg.create_task(worker(3, True))
    except* Exception as eg:
        print("Caught except group")
        for sub in eg.exceptions:
            print("- ", type(sub).__name__, sub)
    print(f"was t1 cancelled?: {t1.cancelled()}")
    print(f"was t2 cancelled?: {t2.cancelled()}")
    print(f"was t3 cancelled?: {t3.cancelled()}")

asyncio.run(failing_main())