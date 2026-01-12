import socket as sc

def echo_server(address):
    sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print(f"Connection from {addr}")
        echo_handler(client)

def echo_handler(client):
    while True:
        data = client.recv(100000)
        if not data:
            break
        client.sendall(b'Got: ' + data)
    print("conn closed")
    client.close()

if __name__ == "__main__":
    echo_server(("", 25000))