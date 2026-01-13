import asyncio

num = 0
lock = asyncio.Lock()

async def offset():
    await asyncio.sleep(0)
    return 1

async def increment():
    global num
    num += await offset()

async def safe_increment():
    async with lock:
        global num
        num += await offset()

async def main():
    tasks = []
    for i in range(100):
        tasks.append(safe_increment())
    await asyncio.gather(*tasks)
    return num

print(asyncio.run(main()))