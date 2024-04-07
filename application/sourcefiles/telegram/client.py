import os
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.qrlogin import QRLogin
from telethon.tl.types import InputPeerUser, User
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError
from dotenv import load_dotenv

from ..database import SQLite
from ..utils import generate_qrcode

load_dotenv()

class UserClient(TelegramClient):
    def __init__(self, session: str = "", *args, **kwargs) -> None:
        self.database = SQLite()
        self.api_id: int = int(os.getenv("API_ID", "API_ID"))
        self.api_hash: str = os.getenv("API_HASH", "API_HASH")
        super().__init__(
            StringSession(session),
            self.api_id,
            self.api_hash,
            system_version="4.16.30-vxCUSTOM",
            device_model="Syncogram Application",
            app_version="0.0.1",
        )
    
    def run_in_loop(self, function):
        return self.loop.run_until_complete(function)

    async def start_client(self):
        if not self.is_connected():
            await self.connect()
        
        print(await self.get_me())


    async def login_by_qrcode(self, dialog, is_primary):
        if not self.is_connected():
            await self.connect()

        qr_login: QRLogin = await self.qr_login()
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
                        await self.sign_in(password=password)
                        r = True
                    except PasswordHashInvalidError:
                        await dialog.update_async()
 
        dialog.open = False
        await dialog.update_async()
        user: User | InputPeerUser = await self.get_me()
        self.database.add_user(
            user.id, # type: ignore
            user.first_name, # type: ignore
            is_primary,
            self.session.save() # type: ignore
        )
        self.disconnect()


    async def logout(self):
        if not self.is_connected():
            await self.connect()
        return await self.log_out()
