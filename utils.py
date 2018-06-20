from urllib.parse import urlparse
from http_parser.parser import HttpParser


def get_headers_data(data):
    """ """
    parser = HttpParser()
    parser.execute(data, len(data))
    url = parser.get_url()
    method = parser.get_method()
    if method == 'CONNECT':
        host, _, port = url.partition(":")
    else:
        url = urlparse(url)
        host, _, port = url.netloc.partition(":")
    port = port and port.isdigit() and int(port) or 80
    return (host, port), method, parser.get_version()
