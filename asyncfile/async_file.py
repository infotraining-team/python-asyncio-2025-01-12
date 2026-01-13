import asyncio

class AsyncFile:
    def __init__(self, filename):
        self.filename = filename

    async def __aenter__(self):
        self.file = await asyncio.to_thread(open, self.filename, mode='rb')
        return self

    async def read_all(self):
        data = await asyncio.to_thread(self.file.read)
        return data

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.to_thread(self.file.flush())
        self.file.close()


