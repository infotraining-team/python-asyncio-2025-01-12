import asyncio

async def run(i, semaphore):
    async with semaphore:
        print(f"{i} working...")
        return await asyncio.sleep(1)

async def main():
    semaphore = asyncio.Semaphore(20)
    await asyncio.gather(*[run(i, semaphore) for i in range(100)])

asyncio.run(main())
