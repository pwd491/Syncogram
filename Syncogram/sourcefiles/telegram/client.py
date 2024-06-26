import asyncio
import platform

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.qrlogin import QRLogin
from telethon.tl.types import InputPeerUser, User
from telethon.errors import (
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    UsernameNotModifiedError,
    UsernameInvalidError,
    UsernameOccupiedError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError
    )
from telethon import functions

from ..database import SQLite
from ..utils import config
from ..utils import logging
from ..utils import generate_qrcode
from ..utils import generate_username
from .environments import API_ID, API_HASH

cfg = config()
logger = logging()

class UserClient(TelegramClient):
    """Custom wraps of Telegram client."""
    @logger.catch()
    def __init__(self, session: str = str()) -> None:
        self.database = SQLite()
        self.api_id: int = int(API_ID)
        self.api_hash: str = API_HASH
        super().__init__(
            StringSession(session),  # type: ignore
            self.api_id,
            self.api_hash,
            device_model=f"{platform.uname().system} {platform.uname().release}",
            app_version=cfg["APP"]["VERSION"],
        )

    @logger.catch()
    async def set_random_username(self, user: User | InputPeerUser) -> User | InputPeerUser:
        """If username is None, generate and set username to account."""
        while True:
            try:
                username = generate_username()
                await self(functions.account.UpdateUsernameRequest(
                    username
                ))
                user.username = username
                break
            except (
                UsernameNotModifiedError,
                UsernameInvalidError,
                UsernameOccupiedError
            ):
                continue
        return user

    @logger.catch()
    async def save_user_data(self, is_primary: bool):
        """Save user data to database"""
        user: User | InputPeerUser = await self.get_me()
        if user.username is None:
            user = await self.set_random_username(user)

        return self.database.add_user(
            user.id,
            is_primary,
            user.username,
            user.phone,
            user.first_name,
            user.last_name,
            int(user.restricted),
            str(user.restriction_reason),
            int(user.stories_hidden),
            int(user.stories_unavailable),
            int(user.contact_require_premium),
            int(user.scam),
            int(user.fake),
            int(user.premium),
            user.photo.photo_id if user.photo is not None else None,
            str(user.emoji_status),
            str(user.usernames),
            user.color,
            str(user.profile_color),
            self.session.save(),
            user.access_hash
        )

    @logger.catch()
    async def login_by_qrcode(self, dialog, is_primary: bool):
        """Create QR image and await for login by url."""
        if not self.is_connected():
            await self.connect()

        qr_login: QRLogin = await self.qr_login()
        r = False
        while not r:
            dialog.qrcode_image.src_base64 = generate_qrcode(qr_login.url)
            dialog.qrcode_image.update()
            try:
                r = await qr_login.wait(60)
            except asyncio.exceptions.TimeoutError:
                try:
                    await qr_login.recreate()
                except ConnectionError:
                    return
            except SessionPasswordNeededError:
                await dialog.input_2fa_password()
                while not r:
                    await dialog.password_inputed_event.wait()
                    password = dialog.password.value
                    try:
                        await self.sign_in(password=password)
                        r = True
                    except PasswordHashInvalidError:
                        await dialog.error()
                    except ConnectionError:
                        return
            except ConnectionError:
                return
        response = await self.save_user_data(is_primary)
        if response == 1555:
            await self.log_out()

        await self.disconnect()
        return response

    @logger.catch()
    async def login_by_phone_number(self, dialog, is_primary: bool):
        """Login by phone number."""
        if not self.is_connected():
            await self.connect()

        try:
            phone = dialog.phone_field.value
            if len(phone) <= 0:
                raise PhoneNumberInvalidError(None)
            login_token = await self.send_code_request(phone=phone)
            await dialog.phone_number_valid()
        except PhoneNumberInvalidError:
            await dialog.phone_number_invalid()
            return PhoneNumberInvalidError

        r = False
        while not r:
            try:
                await dialog.input_code()
                await dialog.password_inputed_event.wait()
                await self.sign_in(login_token, dialog.code_field.value)
                await dialog.phone_code_valid()
                r = True
            except SessionPasswordNeededError:
                await dialog.phone_code_valid()
                await dialog.input_2fa_password()
                while not r:
                    await dialog.password_inputed_event.wait()
                    password = dialog.password.value
                    try:
                        await self.sign_in(password=password)
                        await dialog.password_valid()
                        r = True
                    except PasswordHashInvalidError:
                        await dialog.password_invalid()
                    except ConnectionError:
                        return None
            except PhoneCodeInvalidError:
                await dialog.phone_code_invalid()

        response = await self.save_user_data(is_primary)
        if response == 1555:
            await self.log_out()

        await self.disconnect()
        return response

    @logger.catch()
    async def logout(self) -> bool:
        """Logout from account."""
        if not self.is_connected():
            await self.connect()
        return await self.log_out()

    @logger.catch()
    async def is_user_valid(self) -> bool:
        """Check is user valid."""
        if not self.is_connected():
            await self.connect()
        return await self.is_user_authorized()
