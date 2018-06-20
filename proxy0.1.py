import socket


def headers_parser(data):
    """ """
    data = "".join(str(d) for d in data)
    print(data.strip("\r\n"), sep="\n\n")


def server():
    """ """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 8001))
    s.listen(5)
    print("Running ...")
    while True:
        client, addr = s.accept()
        print("New connection", addr)
        client_handler(client)


def client_handler(client):
    """ """
    data = []
    while True:
        d = client.recv(100)
        if not d:
            break
        data.append(d)
    if data:
        headers_parser(data)
    client.send("HIHI".encode())
    client.close()


if __name__ == "__main__":
    server()
