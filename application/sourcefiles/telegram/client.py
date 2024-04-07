import os
import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.qrlogin import QRLogin
from telethon.tl.types import InputPeerUser, User
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError
from dotenv import load_dotenv

from ..database import SQLite
from ..utils import generate_qrcode

load_dotenv()

class UserClient():
    def __init__(self, session: str | None = None, *args, **kwargs) -> None:
        self.database = SQLite()
        self.api_id: str = os.getenv("API_ID", "API_ID")
        self.api_hash: str = os.getenv("API_HASH", "API_HASH")
        self.session = session
        self.client = TelegramClient(
            StringSession(self.session), # type: ignore
            self.api_id, # type: ignore
            self.api_hash,
            system_version="4.16.30-vxCUSTOM",
            device_model="Syncogram Application",
            app_version="0.0.1",
        )

    async def login_by_qrcode(self, dialog, is_primary):
        if not self.client.is_connected():
            await self.client.connect()

        qr_login: QRLogin = await self.client.qr_login()
        r = False
        while not r:
            dialog.qrcode_image.src_base64 = generate_qrcode(qr_login.url)
            await dialog.update_async()
            try:
                r = await qr_login.wait(60)
            except asyncio.exceptions.TimeoutError:
                await qr_login.recreate()
            except SessionPasswordNeededError:
                await dialog.input_2fa_password()
                while not r:
                    await dialog.password_inputed_event.wait()
                    password = dialog.password.value
                    try:
                        await self.client.sign_in(password=password)
                        r = True
                    except PasswordHashInvalidError:
                        await dialog.update_async()
 
        dialog.open = False
        await dialog.update_async()
        user: User | InputPeerUser = await self.client.get_me()
        self.database.add_user(
            user.id, # type: ignore
            user.first_name, # type: ignore
            is_primary,
            self.client.session.save() # type: ignore
        )
        self.client.disconnect()


    async def logout(self):
        if not self.client.is_connected():
            await self.client.connect()
        return await self.client.log_out()
        

    # async def login_by_phone_number(self):
    #     await self.client.connect()
    #     phone = "79604122155"
    #     phone_code = await self.client.send_code_request(phone)
    #     phone_code_hash = phone_code.phone_code_hash

    #     code: str = input("Input code:")
    #     try:
    #         await self.client.sign_in(phone, code=code, phone_code_hash=phone_code_hash)
    #     except SessionPasswordNeededError:
    #         password = input("Enter password:")
    #         await self.client.sign_in(password=password)
    #         user = await self.client.get_me()
    #         session = self.client.session.save()
    #         print(session)
    #         result = self.database.add_user(id=user.id, name=user.first_name, is_primary=1,session=session)
    #         print(result)

  
