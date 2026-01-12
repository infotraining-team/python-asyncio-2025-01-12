import asyncio

async def echo_server(address):
    server = await asyncio.start_server(echo_handler, address[0], address[1])
    async with server:
        await server.serve_forever()

async def echo_handler(reader, writer):
    while True:
        data = await reader.read(10000)
        if not data:
            break
        writer.write(b'Got: ' + data)
        await writer.drain()
    print("conn closed")


if __name__ == "__main__":
    asyncio.run(echo_server(("", 25000)))