import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
from telethon.tl.types import User


load_dotenv()

class TelegramUserClient(TelegramClient):
    def __init__(self, *args, **kwargs):
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash: str = str(os.getenv('API_HASH'))

        self.client = TelegramClient(
            "test",
            self.api_id,
            self.api_hash,
            system_version="4.16.30-vxCUSTOM",

        )

    async def connect(self):
        return await self.client.connect()

    async def login(self):
        await self.client.connect()
        phone = "79604122155"
        phone_code = await self.client.send_code_request(phone)
        phone_code_hash = phone_code.phone_code_hash

        code = input("Input code:")
        try:
            await self.client.sign_in(phone, code=code, phone_code_hash=phone_code_hash)
        except SessionPasswordNeededError:
            password = input("Enter password:")
            await self.client.sign_in(password=password)
            print("Success!")
        
        print(await self.client.get_me())
        

    async def check(self):
        print(self.client)


async def main():
    abs = TelegramUserClient()
    await abs.login()
    abs.client.run_until_disconnected()

asyncio.run(main())