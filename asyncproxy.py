import asyncio
from urllib.parse import urlparse
import socket


class Client(asyncio.Protocol):
    loop = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data)
        data = data.decode().split("\r\n")
        host = data[0].split()[1]
        print(host)
        host = urlparse(host)
        print(host)
        netloc = host.netloc or host.path
        host, port = netloc.split(":")
        port = int(port)
        asyncio.ensure_future(self.co(host, port, data))

    async def co(self, host, port, data):
        r, w = await asyncio.open_connection(host=host, port=port, loop=self.loop)
        dd = "\r\n".join(data)

        w.write(dd.encode())
        await w.drain()
        while True:
            d = await r.read(n=8192)
            if not d:
                break
            self.transport.write(d)
        w.close()
        self.transport.close()


loop = asyncio.get_event_loop()
Client.loop = loop
server = loop.create_server(Client, '127.0.0.1', 8001)

loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
