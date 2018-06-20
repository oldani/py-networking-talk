from gevent import socket, monkey; monkey.patch_all()
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from gevent.server import StreamServer
from gevent.select import select


class Proxy(BaseHTTPRequestHandler):

    CRLF = "\r\n"
    buffersize = 8192

    def __init__(self, soc, address):
        super().__init__(soc, address, '')

    def _conect_to(self, netloc):
        """ """
        host, _, port = netloc.partition(":")
        port = port and port.isdigit() and int(port) or 80
        try:
            print(host, port, netloc)
            self.soc.connect((host, port))
            return True
        except Exception as e:
            # self.log_error(e)
            print(e)
        return

    def read_write(self, max_idling=20):
        """ """
        count = 0
        while True:
            count += 1
            rlist, *_ = select([self.connection, self.soc], [], [])

            if rlist:
                for s in rlist:
                    sock_out = self.connection if s is self.soc else self.soc
                    try:
                        data = s.recv(self.buffersize)
                        if data:
                            sock_out.send(data)
                            count = 0
                    except Exception as e:
                        print(e)
                        break
            if count == max_idling:
                break

    def do_GET(self):
        """ """
        url = urlparse(self.path, 'http')

        if not (url.scheme == 'http' or url.netloc):
            self.send_error(400, f"Bad url {self.path}")
        self.connection
        self.soc = socket.socket()

        try:
            if self._conect_to(url.netloc):
                self.log_request()
                self.soc.send(f"{self.requestline}{self.CRLF}".encode())
                del self.headers['Proxy-Connection']
                del self.headers['Connection']
                self.headers['Connection'] = 'close'
                for key, val in self.headers.items():
                    self.soc.send(f"{key}: {val}{self.CRLF}".encode())
                self.soc.send(f"{self.CRLF * 2}".encode())
                self.read_write()
        except Exception as e:
            print(e)
        finally:
            self.soc.close()
            self.connection.close()
    do_POST = do_GET

    def do_CONNECT(self):
        """ """
        self.soc = socket.socket()
        url = urlparse(self.path, 'https')
        try:
            if self._conect_to(url.path):
                self.log_request(200)
                self.connection.send(f"{self.protocol_version} 200 Connection established{self.CRLF * 2}".encode())
                self.read_write(max_idling=300)
        except Exception as e:
            print(e)
        finally:
            self.soc.close()
            self.connection.close()


def run(addrs):
    """ """
    server = StreamServer(addrs, Proxy)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    run(("127.0.0.1", 8001))
