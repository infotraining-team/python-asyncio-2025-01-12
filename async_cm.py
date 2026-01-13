import asyncio

class AsyncCM:
    def __init__(self):
        pass

    def __enter__(self):
        print("Entering sync")
        # can't use coroutines
        ## await asyncio.sleep(0.5)
        return self

    async def __aenter__(self):
        print("Entering CM")
        await asyncio.sleep(0.5)
        return self

    async def something(self):
        print("Doing something")

    async def __aexit__(self, ext, exc, tb):
        print("Cleaning")

    def __exit__(self, ext, exc, tb):
        print("Sync Cleaning")

async def main():
    async with AsyncCM() as acm:
        await acm.something()

    print("Now synchronous")
    with AsyncCM() as acm:
        await acm.something()
        pass

asyncio.run(main())
