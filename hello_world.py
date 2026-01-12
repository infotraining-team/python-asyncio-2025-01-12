import asyncio

async def hello_world():
    print("Hello World!")
    await asyncio.sleep(1)

asyncio.run(hello_world())