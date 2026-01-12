import asyncio
import socket
from keyword import kwlist


async def check(domain):
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)

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

async def main_check():
    names = (kw + ".pl" for kw in kwlist)
    #print(list(names))
    tasks = [asyncio.create_task(check(domain)) for domain in names]
    for coro in asyncio.as_completed(tasks):
        domain, found = await coro
        mark = "+" if found else "-"
        print(f"{mark} {domain}")

#asyncio.run(check("global.pl"))
asyncio.run(main_check())