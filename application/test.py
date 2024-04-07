import asyncio
from sourcefiles import TelegramTasksManager


async def main():
    x = TelegramTasksManager()
    await x.sync_saved_messages()

asyncio.run(main())
