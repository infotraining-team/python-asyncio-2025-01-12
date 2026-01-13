import asyncio

async def counter(n):
    while n >= 0:
        await asyncio.sleep(0.2)
        yield n
        n -= 1

class BigCounter:
    def __init__(self, n):
        self.n = n

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.n > 0:
            self.n -= 1
            await asyncio.sleep(0.1)
            return self.n
        else:
            raise StopAsyncIteration


async def main():
    async for i in counter(10):
        print(i)

    async for i in BigCounter(10):
        print(i)

asyncio.run(main())