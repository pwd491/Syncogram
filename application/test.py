import asyncio
from sourcefiles import Manager


x = Manager()

async def main():
    await x.build()

asyncio.run(main())