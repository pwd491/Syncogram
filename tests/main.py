import asyncio
import datetime
import random
import time
import re
from typing import Dict, Callable, Coroutine
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl import types
from telethon.tl.functions import messages
from telethon import events
from telethon import errors
from telethon.tl import custom
from telethon.tl import patched
from telethon.helpers import TotalList

from environments import API_HASH, API_ID, R_SESSION, S_SESSION, M_SESSION

# sender = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)

def autoconnect(func: Coroutine):
    """Decorator got token and connect user to server."""
    async def wrapper(*args):
        sender = TelegramClient(StringSession(S_SESSION), API_ID, API_HASH)
        recepient = TelegramClient(StringSession(R_SESSION), API_ID, API_HASH)
        if not sender.is_connected():
            await sender.connect()
        if not recepient.is_connected():
            await recepient.connect()
        return await func(*args, sender=sender, recepient=recepient)
    return wrapper

def find_deep_links_hashes(message: str) -> list[str]:
    """
    Regex string for search deep invite links. Delete hashes duplicates. Return
    list of searched hashes.
    
    t.me/+<hash>
    t.me/joinchat/<hash> (legacy)
    tg://join?invite=<hash>
    """
    pattern = re.compile(
        r"(?:t|tg|telegram)(?:\.|\:)(?:me/|dog/|//)(?:\+|joinchat/|join\?invite=)([\w]+)",
    )
    return list(dict.fromkeys(pattern.findall(message)))

@autoconnect
async def main(ui: str, **kwargs):
    sender: TelegramClient = kwargs["recepient"]
    recepient: TelegramClient = kwargs["sender"]

    def is_already_joined(channel_id: int) -> bool:
        """Looking channel or group in Recepient chat list."""
        for channel in recepient_dialogs:
            if isinstance(channel, types.Channel):
                if channel.entity.id == channel_id:
                    return True
        return False

    async def channels() -> None:
        for channel in sender_dialogs:
            if isinstance(channel.entity, types.Channel):
                if channel.entity.username is None and \
                    channel.entity.usernames is None:
                    if is_already_joined(channel.entity.id):
                        continue
                    channel_and_link.setdefault(channel.entity.title)
                    channels_to_find.append(channel)

    async def find_unique_hashes_in_overall_messages():
        timeout = 10 if len(channels_to_find) > 50 else 5
        for k, channel in enumerate(channels_to_find, 1):
            await asyncio.sleep(timeout)
            try:
                last_50_messages = await sender.get_messages(
                    channel.input_entity, limit=50
                )
            except errors.FloodWaitError as spam:
                print(spam)
                print(k)
                await asyncio.sleep(spam.seconds)
                last_50_messages = await sender.get_messages(
                    channel.input_entity, limit=50
                )

            text = []
            message: patched.Message
            for message in last_50_messages:
                if message.text:
                    text.append(message.text)
        check = "\n".join(text)
        hashes.extend(find_deep_links_hashes(check))

    async def check_deep_link_valid():
        timeout = 10 if len(hashes) > 50 else 5
        latest_client = sender
        for invite_hash in hashes:
            latest_client = sender if latest_client == recepient else recepient
            await asyncio.sleep(timeout)
            try:
                request = latest_client(
                    messages.CheckChatInviteRequest(
                        hash=invite_hash
                    )
                )
                chat: types.ChatInvite = await request
            except (
                errors.InviteHashEmptyError,
                errors.InviteHashExpiredError,
                errors.InviteHashInvalidError,
            ):
                pass
            except errors.FloodWaitError as spam:
                print(spam)
                await asyncio.sleep(spam.seconds)
                chat = await request

            if chat.title in channel_and_link:
                channel_and_link[chat.title] = invite_hash

    async def join_to_channels_or_groups():
        timeout = 10 if len(channel_and_link) > 50 else 5
        for key, value in channel_and_link.items():
            if value is not None:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        messages.ImportChatInviteRequest(
                            hash=value
                        )
                    )
                except (
                    errors.UserAlreadyParticipantError,
                    errors.InviteHashInvalidError,
                    errors.InviteHashExpiredError,
                    errors.InviteHashEmptyError,
                    errors.UsersTooMuchError,
                ):
                    pass
                except errors.ChannelsTooMuchError as e:
                    print(e)
                except errors.InviteRequestSentError:
                    print("Эта я типа успешно присоединился.")
                except errors.FloodWaitError as flood:
                    print(flood)
                    print("Время паузы увеличино: ", timeout, timeout + 5)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    await recepient(
                        messages.ImportChatInviteRequest(
                            hash=value
                        )
                    )

    sender_dialogs: list[custom.dialog.Dialog] = await sender.get_dialogs()
    recepient_dialogs: list[custom.dialog.Dialog] = await recepient.get_dialogs()

    channels_to_find: list[custom.dialog.Dialog] = []
    channel_and_link: Dict[str, str] = {}
    hashes: list[str] = []

    await channels()
    await find_unique_hashes_in_overall_messages()
    await check_deep_link_valid()
    await join_to_channels_or_groups()
if __name__ == "__main__":
    asyncio.run(main("asd"))