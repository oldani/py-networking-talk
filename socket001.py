from gevent import monkey; monkey.patch_all()
import socket
from threading import Thread


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8001))
    sock.listen(5)
    while True:
        client, addrs = sock.accept()
        Thread(target=handler, args=(client, addrs)).start()
        # handler(client, addrs)


def handler(client, addrs):
    print(addrs)
    while True:
        data = client.recv(100)
        if not data:
            break
        client.sendall(data)


if __name__ == "__main__":
    main()
