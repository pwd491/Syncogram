from sourcefiles import SQLite
from sourcefiles import UserClient
import asyncio

x = UserClient()

async def main():
    await x.start_client()

asyncio.run(main())