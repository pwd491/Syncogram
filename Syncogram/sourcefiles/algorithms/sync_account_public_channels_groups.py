import asyncio

from telethon import errors
from telethon.tl.functions import channels, messages
from telethon.tl import types
from telethon.tl.custom.dialog import Dialog

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_public_channels_and_groups(ui: Task, **kwargs):
    """
    The algorithm for synchronizing public channels, 
    the status of pinning and archiving.
    """
    def get_public_channels(dialogs: list[Dialog]) -> list[Dialog]:
        lst: list[Dialog] = []
        dialog: Dialog
        for dialog in dialogs:
            if not isinstance(dialog.entity, types.Chat) \
                and not dialog.is_user \
                    and dialog.entity.username:
                lst.append(dialog)
        return lst

    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    source = await sender.get_dialogs()
    recepient_channels = await recepient.get_dialogs()

    channels_list: list[Dialog] = get_public_channels(source)
    recepient_channels: list[Dialog] = get_public_channels(recepient_channels)
    r_channels: list[int] = [channel.entity.id for channel in recepient_channels]

    ui.progress_counters.visible = True
    ui.total = len(channels_list) - 1

    timeout = 10 if len(channels_list) <= 30 else 15
    timeout_adc = 2.5

    channel: Dialog
    for channel in channels_list:
        if channel.entity.id not in r_channels:
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        channels.JoinChannelRequest(channel.entity.username)
                    )
                    break
                except errors.ChannelsTooMuchError as error:
                    logger.critical(error)
                    ui.message(error.message)
                    ui.unsuccess(error)
                    return
                except (
                    errors.ChannelInvalidError,
                    errors.ChannelPrivateError
                ) as error:
                    logger.error(error)
                    ui.message(f"Unsuccess join to: {channel.entity.title}")
                    break
                except errors.InviteRequestSentError:
                    break
                except errors.FloodWaitError as flood:
                    logger.warning(flood)
                    ui.message(flood)
                    ui.cooldown(flood)
                    timeout += 5
                    await asyncio.sleep(flood.seconds)
                    ui.uncooldown()

            if channel.archived:
                while True:
                    try:
                        await asyncio.sleep(timeout_adc)
                        await recepient.edit_folder(channel.entity.username, 1)
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood)
                        ui.cooldown(flood)
                        timeout_adc += 5
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()

            if channel.pinned:
                while True:
                    try:
                        await asyncio.sleep(timeout_adc)
                        await recepient(messages.ToggleDialogPinRequest(
                            channel.entity.username,
                            True
                        ))
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood)
                        ui.cooldown(flood)
                        timeout_adc += 5
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()
        ui.value += 1

    ui.success()
