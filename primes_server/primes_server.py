import asyncio
from primes import primes_up_to

from concurrent.futures import ProcessPoolExecutor

pool = ProcessPoolExecutor()

async def primes_server(address):
    server = await asyncio.start_server(primes_handler, address[0], address[1])
    async with server:
        await server.serve_forever()

async def primes_handler(reader, writer):
    data = await reader.read(10000)
    try:
        n = int(data)
    except ValueError:
        n = 2
    # blocking,
    #results = primes_up_to(n)
    # Solution 1:
    # results = await asyncio.to_thread(primes_up_to, n)
    # Solution 2: process pool
    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(pool, primes_up_to, n)
    writer.write(b'Got: ' + str(results[-1]).encode("utf-8"))
    await writer.drain()
    writer.close()

if __name__ == "__main__":
    asyncio.run(primes_server(("", 25000)))