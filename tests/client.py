import os
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
from telethon.tl.types import User
from qrcode import QRCode


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
        self.qr = QRCode()

    def gen_qr(self, token:str):
        self.qr.clear()
        self.qr.add_data(token)
        self.qr.print_ascii()
        

    def display_url_as_qr(self, url):
        print(url)
        self.gen_qr(url)
    
    async def log_by_qr(self):
        if not self.client.is_connected():
            await self.client.connect()
        qr_login = await self.client.qr_login()
        r = False
        while not r:
            self.display_url_as_qr(qr_login.url)
        # Important! You need to wait for the login to complete!
            try:
                r = await qr_login.wait(60)
            except TimeoutError:
                await qr_login.recreate()
            except SessionPasswordNeededError:
                password = input("Input pass: ")
                await self.client.sign_in(password=password)
        

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
    x = TelegramUserClient()
    await x.log_by_qr()
    x.run_until_disconnected()

asyncio.run(main())

x.run_until_disconnected()

