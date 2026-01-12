import asyncio
import socket
import ssl
import time

URLS = [
    "www.google.com", "www.python.org", "www.github.com",
    "www.microsoft.com", "www.apple.com", "www.amazon.com",
    "www.cloudflare.com", "www.wikipedia.org", "www.stackoverflow.com",
    "www.example.com"
]
PORT = 443  # HTTPS

def sync_fetch(url):
    # Create a standard SSL context
    context = ssl.create_default_context()

    # Standard blocking socket
    with socket.create_connection((url, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=url) as ssock:
            # Send simple HTTP/1.0 request (closes connection automatically)
            request = f"GET / HTTP/1.0\r\nHost: {url}\r\n\r\n"
            ssock.sendall(request.encode())

            # Read first 1024 bytes (enough for headers)
            data = ssock.recv(1024)
            print(f"Sync: Received from {url}")

def fetch_sync():
    print("Fetch sync:")
    start = time.perf_counter()
    for url in URLS:
        sync_fetch(url)
    t = time.perf_counter() - start
    print(f"Took {t} s")

async def async_fetch(url):
    try:
        reader, writer = await asyncio.open_connection(url, PORT, ssl=True)
        request = f"GET / HTTP/1.0\r\nHost: {url}\r\n\r\n"
        writer.write(request.encode())
        await writer.drain()
        # Read first 1024 bytes (enough for headers)
        data = await reader.read(1024)
        print(f"Async: Received from {url}")
    except ssl.SSLError:
        print("SSL ERROR")

async def fetch_async():
    print("Fetch async:")
    start = time.perf_counter()
    #for url in URLS:
    #    await async_fetch(url)
    await asyncio.gather(*[async_fetch(url) for url in URLS])
    t = time.perf_counter() - start
    print(f"Took {t} s")

async def main():
    await fetch_async()
    fetch_sync()


asyncio.run(main())