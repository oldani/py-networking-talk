import time
import asyncio
import aiohttp
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
conn = aiohttp.TCPConnector(limit=0)
n = 0
url = "https://a99xrnggp2.execute-api.us-east-1.amazonaws.com/dev"
# url = "http://127.0.0.1:8000"


async def main():
    """ """
    async with aiohttp.ClientSession(connector=conn) as session:
        while True:
            async with session.get(url) as r:
                pass
            global n
            n += 1


def monitor():
    while True:
        time.sleep(1)
        global n
        print(f"{n} reqs/sec")
        n = 0


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, monitor)
    loop.run_until_complete(main())
