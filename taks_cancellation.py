import asyncio
import time

async def cancellable(delay):
    print(f"Sleeping for {delay}")
    try:
        await asyncio.sleep(delay)
        #time.sleep(delay)
    except asyncio.CancelledError:
        print("got cancelled")
        return 0
    print("Woke from sleep")
    return 42

async def main():
    task = asyncio.create_task(cancellable(4))
    print("Task is running")
    await asyncio.sleep(1)
    task.cancel()
    print("Task is cancelled")
    res = await task
    print(res)

asyncio.run(main())