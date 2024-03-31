import os
import asyncio

from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from dotenv import load_dotenv

from sql import SQLite
load_dotenv()


class UserClient(TelegramClient):
    def __init__(self, *args, **kwargs) -> None:
        self.database = SQLite()
        self.api_id = os.getenv("API_ID", "API_ID")
        self.api_hash = os.getenv("API_HASH")

        self.client = TelegramClient(
            StringSession(),
            str(self.api_id),
            self.api_hash,
            system_version="4.16.30-vxCUSTOM",
            device_model="Syncogram Application",
            app_version="0.0.1",
        )

    async def login_by_qrcode(self):
        if not self.client.is_connected():
            await self.client.connect()
        qr_login = await self.client.qr_login()
        r = False
        while not r:
            # self.display_url_as_qr(qr_login.url)
            try:
                r = await qr_login.wait(60)
            except TimeoutError:
                await qr_login.recreate()
            except SessionPasswordNeededError:
                password = input("Input pass: ")
                await self.client.sign_in(password=password)

    async def login_by_phone_number(self):
        await self.client.connect()
        phone = "79604122155"
        phone_code = await self.client.send_code_request(phone)
        phone_code_hash = phone_code.phone_code_hash

        code: str = input("Input code:")
        try:
            await self.client.sign_in(phone, code=code, phone_code_hash=phone_code_hash)
        except SessionPasswordNeededError:
            password = input("Enter password:")
            await self.client.sign_in(password=password)
            user = await self.client.get_me()
            session = self.client.session.save()
            print(session)
            result = self.database.add_user(id=user.id, name=user.first_name, is_primary=1,session=session)
            print(result)

    async def check(self):
        print(await self.client.get_me())


async def main():
    x = UserClient()
    await x.login_by_phone_number()

asyncio.run(main())