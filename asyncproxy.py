import asyncio
from utils import get_headers_data


class Client(asyncio.Protocol):
    loop = None
    CRLF = "\r\n"
    buffersize = 8192

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, excep):
        """ """
        if excep:
            print(excep)
        self.transport.close()
        if hasattr(self, "connection"):
            self.connection.close()

    def data_received(self, data):
        """ """
        self.data = data
        address, method, self.version = get_headers_data(data)
        asyncio.ensure_future(self.handle_connection(address, method))

    async def handle_connection(self, address, method):
        """ """
        print(address, method, self.data)
        mname = f"do_{method}"
        if not hasattr(self, mname):
            return
        method = getattr(self, mname)
        try:
            reader, self.writer = await asyncio.open_connection(host=address[0],
                                                                port=address[1],
                                                                loop=self.loop)
        except Exception as e:
            print(e)
        await method(reader, self.writer)

    async def do_CONNECT(self, reader, writer):
        """ """
        out = (f"HTTP/{'.'.join(str(n) for n in self.version)} "
               f"200 Connection established{self.CRLF * 2}".encode())
        self.transport.write(out)
        self.connection = self.transport.get_extra_info('socket')
        self.loop.add_reader(self.connection, self.read_write, writer)
        data = await reader.read(n=self.buffersize)
        self.transport.write(data)
        self.loop.add_reader(self.connection, self.read_write, writer)

    def read_write(self, writer):
        """ """
        asyncio.ensure_future(self._read_write(writer))

    async def _read_write(self, writer):
        """ """
        while True:
            data = await self.loop.sock_recv(self.connection, self.buffersize)
            if not data:
                break

            writer.write(data)
            await writer.drain()
        self.connection_lost(None)

    async def do_GET(self, reader, writer):
        """ """
        writer.write(self.data)
        await writer.drain()
        while True:
            data = await reader.read(n=8192)
            if not data:
                break
            self.transport.write(data)
        writer.close()
        self.transport.close()


loop = asyncio.get_event_loop()
Client.loop = loop
server = loop.create_server(Client, '127.0.0.1', 8001)

loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
