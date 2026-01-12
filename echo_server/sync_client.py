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

if __name__ == "__main__":
    import multiprocessing as mp
    p1 = mp.Process(target=echo_client, args=((0.5, "Leszek")))
    p2 = mp.Process(target=echo_client, args=((0.5, "Robert")))
    p3 = mp.Process(target=echo_client, args=((0.5, "Bruno")))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()