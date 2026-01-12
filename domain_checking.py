import asyncio
import socket
from keyword import kwlist


async def check(domain):
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        print("not a domain")
        return
    print("domain is active")

async def coro(delay, crash=False):
    print(f"Starting coro with delay {delay}")
    await asyncio.sleep(delay)
    if crash:
        raise ValueError
    else:
        return 42*delay

async def main():
    tasks = [asyncio.create_task(c) for c in (coro(3), coro(2), coro(4), coro(1))]
    for c in asyncio.as_completed(tasks):
        res = await c
        print(res)

print(kwlist)
asyncio.run(check("awdawdawda"))