import os
import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError
from dotenv import load_dotenv

from ..database import SQLite
from ..utils import generate_qrcode

load_dotenv()

class UserClient(TelegramClient):
    def __init__(self, AuthDialog, *args, **kwargs) -> None:
        self.database = SQLite()
        self.dialog = AuthDialog
        self.api_id = os.getenv("API_ID", "API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.session = kwargs
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
            self.dialog.wrapper.content.src_base64 = generate_qrcode(qr_login.url)
            await self.dialog.update_async()
            try:
                r = await qr_login.wait(60)
            except SessionPasswordNeededError:
                password = input("Input password:")
                try:
                    await self.client.sign_in(password=password)
                    r = True
                except PasswordHashInvalidError:
                    print("Wrong password! Try again.")
                    password_again = input("Input password again: ")
                    await self.client.sign_in(password=password_again)
                    r = True
            except asyncio.exceptions.TimeoutError:
                await qr_login.recreate()

        self.dialog.open = False
        await self.dialog.update_async()
        print(await self.client.get_me())
        





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
        await self.client.connect()
        return await self.client.get_me()
  
