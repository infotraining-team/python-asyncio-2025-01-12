import asyncio

async def hello():
    print("Starting hello")
    await asyncio.sleep(5)
    print("Hello from async")

async def just_coro():
    print("Starting task")
    await asyncio.sleep(1)
    print("In the middle")
    await asyncio.sleep(1)
    print("End")

async def main():
    await asyncio.gather(hello(), just_coro(), just_coro())

print("Hello: ", type(hello))
print("Hello(): ", type(hello()))
asyncio.run(main())