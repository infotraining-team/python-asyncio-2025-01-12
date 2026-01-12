import asyncio

async def coro1(n):
    print("Starting coro1")
    await asyncio.sleep(n)
    return 42*n

async def main():
    result = await asyncio.gather(coro1(1), coro1(2), coro1(3))
    print(result)

asyncio.run(main())