import socket as sc
import time

def echo_client(delay, client_id):
    print(f"Echo client {client_id}")
    sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    sock.connect(('localhost', 25000))
    print(f"{client_id} connected")

    while True:
        sock.send(f'Hello from client {client_id}'.encode('utf-8'))
        resp = sock.recv(1000)
        print(f"{client_id} got: " + str(resp))
        time.sleep(delay)

echo_client(1, "Leszek")