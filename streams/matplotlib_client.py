import asyncio
import threading
import json
import httpx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

x_data = [deque(maxlen=50), deque(maxlen=50)]
y_data = [deque(maxlen=50), deque(maxlen=50)]

async def consume_stream(i):
    url = "http://127.0.0.1:8000/stream-resume"
    last_seen_id = 0
    while True:
        try:
            connect_url = f"{url}?last_id={last_seen_id}"
            print("Connecting")
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", connect_url) as response:
                    print("Connection established")
                    async for chunk in response.aiter_text():
                        try:
                            data = json.loads(chunk)
                            print(f"Got point {data['id']}, x: {data['x']}, y: {data['y']}")
                            last_seen_id = data["id"]
                            x_data[i].append(data["x"])
                            y_data[i].append(data["y"])
                        except json.JSONDecodeError:
                            print("Failed to parse line")
        except Exception as e:
            print("Connection lost, retrying")
            await asyncio.sleep(3)

async def network():
    await asyncio.gather(consume_stream(0), consume_stream(1))

def update_plot(frame):
    plt.cla()
    plt.plot(list(x_data[0]), list(y_data[0]))
    plt.plot(list(x_data[1]), list(y_data[1]))

def start_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(network())

if __name__ == "__main__":
    t = threading.Thread(target=start_loop, daemon=True)
    t.start()
    fig = plt.figure()
    ani = FuncAnimation(fig, update_plot, interval=100)
    print("Start GUI")
    plt.show()