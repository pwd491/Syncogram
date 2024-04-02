import os
import asyncio
import telethon

from telethon.sessions import StringSession
from flet import Image, TextField
from dotenv import load_dotenv

from utils import generate_qrcode
from sql import SQLite

load_dotenv()

class UserClient(telethon.TelegramClient):
    def __init__(self, AuthDialog, *args, **kwargs) -> None:
        self.database = SQLite()
        self.dialog = AuthDialog
        self.api_id = os.getenv("API_ID", "API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.session = kwargs
        self.client = telethon.TelegramClient(
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
                r = await qr_login.wait(10)
                await self.dialog.update_async()
            except asyncio.exceptions.TimeoutError:
                await qr_login.recreate()
                await self.dialog.update_async()
            except telethon.errors.SessionPasswordNeededError:
                link = self.client.sign_in
                await self.dialog.auth2fa(function=link)
            except telethon.errors.PasswordHashInvalidError:
                self.dialog.wrapper.content.border_color = "red"
                await self.dialog.auth2fa(function=link)

        await self.dialog.clean_async()
        self.dialog.open = False
        self.dialog.snack_bar.open = True
        print(r)
        return r





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
  
