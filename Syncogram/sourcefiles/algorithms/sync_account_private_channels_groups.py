import asyncio
import re

from telethon import errors
from telethon.tl import custom
from telethon.tl import patched
from telethon.tl import types
from telethon.tl.functions import messages

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
def find_deep_links_hashes(message: str) -> list[str]:
    """
    Regex string for search deep invite links. Delete hashes duplicates. Return
    list of searched hashes.
    
    t.me/+<hash>
    t.me/joinchat/<hash> (legacy)
    tg://join?invite=<hash>
    """
    pattern = re.compile(
        r"(?:t|tg|telegram)(?:\.|\:)(?:me/|dog/|//)(?:\+|joinchat/|join\?invite=)([\w-]+)(?<!_)",
    )
    return list(dict.fromkeys(pattern.findall(message)))

@logger.catch()
@autoconnect
async def sync_private_channels_and_groups(ui: Task, **kwargs):
    """
    The algorithm for synchronizing private channels and groups, 
    the status of pinning and archiving.
    """
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    def is_all_founded() -> bool:
        if None in channel_and_link.values():
            return False
        return True

    async def __get_dialogs(client: UserClient) -> None | list[custom.dialog.Dialog]:
        while True:
            try:
                source: list[custom.dialog.Dialog] = await client.get_dialogs()
                break
            except (
                errors.InputConstructorInvalidError,
                errors.OffsetPeerIdInvalidError,
                errors.SessionPasswordNeededError,
                errors.TimeoutError
            ) as error:
                logger.critical(error)
                ui.unsuccess("It is not possible to get a list of the sender's bots.")
                ui.message("It is not possible to get a list of the sender's bots.")
                return
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.cooldown(flood)
                asyncio.sleep(flood.seconds)
                ui.uncooldown()
        return source

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
        ui.message(f"Number of private channels: {len(channels_to_find)}")

    async def find_unique_hashes_in_overall_messages():
        length = len(channels_to_find)
        timeout = 10 if length > 50 else 5
        text = []
        ui.message("Search for links to join through all channels.")
        ui.total = length
        ui.value = 0
        ui.progress_counters.visible = True
        for channel in channels_to_find:
            while True:
                try:
                    await asyncio.sleep(timeout)
                    last_50_messages = await sender.get_messages(
                        channel.input_entity, limit=5
                    )
                    ui.value += 1
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            message: patched.Message
            for message in last_50_messages:
                if message.text:
                    text.append(message.text)
        check = "\n".join(text)
        hashes.extend(find_deep_links_hashes(check))

    async def check_deep_link_valid():
        timeout = 10 if len(hashes) > 50 else 5
        latest_client = sender
        ui.message(f"The number of unique links found to join: {len(hashes)}")
        ui.message("The search for your private channels begins.")
        ui.total = len(hashes)
        ui.value = 0
        for invite_hash in hashes:
            if is_all_founded():
                break
            latest_client = sender if latest_client == recepient else recepient
            while True:
                try:
                    await asyncio.sleep(timeout)
                    chat: types.ChatInvite | types.ChatInvitePeek | types.ChatInviteAlready \
                        = await latest_client(
                        messages.CheckChatInviteRequest(
                            hash=invite_hash
                        )
                    )
                    ui.value += 1
                    break
                except (
                    errors.InviteHashEmptyError,
                    errors.InviteHashExpiredError,
                    errors.InviteHashInvalidError,
                ) as error:
                    ui.message(f"The hash: [{invite_hash}] is invalid.\n{error}")
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            if isinstance(chat, (types.ChatInvitePeek, types.ChatInviteAlready)):
                if chat.chat.title in channel_and_link:
                    if channel_and_link[chat.chat.title] is None:
                        channel_and_link[chat.chat.title] = invite_hash
                        ui.message(f"{chat.chat.title} was founded!")
            else:
                if chat.title in channel_and_link:
                    if channel_and_link[chat.title] is None:
                        channel_and_link[chat.title] = invite_hash
                        ui.message(f"{chat.title} was founded!")

    async def join_to_channels_or_groups():
        length = len(channel_and_link)
        timeout = 10 if length > 50 else 5
        ui.total = length
        ui.value = 0
        ui.progress_counters.visible = True
        for key, value in channel_and_link.items():
            if value is not None:
                while True:
                    try:
                        await asyncio.sleep(timeout)
                        await recepient(
                            messages.ImportChatInviteRequest(
                                hash=value
                            )
                        )
                        ui.value += 1
                        break
                    except (
                        errors.UserAlreadyParticipantError,
                        errors.InviteHashInvalidError,
                        errors.InviteHashExpiredError,
                        errors.InviteHashEmptyError,
                        errors.UsersTooMuchError,
                    ) as error:
                        logger.error(error)
                        ui.message(error, True)
                        break
                    except errors.ChannelsTooMuchError as error:
                        logger.critical(error)
                        ui.message(error)
                        return
                    except errors.InviteRequestSentError:
                        ui.message(f"The application for membership has been successfully submitted: {key}")
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood)
                        timeout += 5
                        ui.cooldown(flood)
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()
        ui.message(f"{ui.value} / {ui.total} was founded.")
        for key, value in channel_and_link.items():
            if value is None:
                ui.message(f"{key} was not found.")

    sender_dialogs: list[custom.dialog.Dialog] = await __get_dialogs(sender)
    recepient_dialogs: list[custom.dialog.Dialog] = await __get_dialogs(recepient)

    if sender_dialogs is None or recepient_dialogs is None:
        ui.unsuccess()
        return
    channels_to_find: list[custom.dialog.Dialog] = []
    channel_and_link: dict[str, str] = {}
    hashes: list[str] = []

    await channels()
    await find_unique_hashes_in_overall_messages()
    await check_deep_link_valid()
    await join_to_channels_or_groups()

    ui.success()