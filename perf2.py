import time
import asyncio
import uvloop
from requests_threads import AsyncSession


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
url = "http://52.186.121.126:8000"
n = 0


async def main():
    while True:
        await session.get(url)
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
    session = AsyncSession(n=1000, loop=loop)
    try:
        loop.run_in_executor(None, monitor)
        # loop.run_until_complete(main())
        session.run(main)
    except KeyboardInterrupt:
        loop.close()
