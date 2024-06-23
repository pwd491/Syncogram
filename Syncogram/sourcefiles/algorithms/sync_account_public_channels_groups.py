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
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    source = await sender.get_dialogs()
    channels_list: list[Dialog] = []

    dialog: Dialog
    for dialog in source:
        if not isinstance(dialog.entity, types.Chat) \
            and not dialog.is_user \
                and dialog.entity.username:
            channels_list.append(dialog)

    ui.progress_counters.visible = True
    ui.total = len(channels_list)

    channel: Dialog
    try:
        for i, channel in enumerate(channels_list, 1):
            await asyncio.sleep(12)
            await recepient(
                channels.JoinChannelRequest(channel.entity.username)
            )
            if channel.archived:
                await asyncio.sleep(2.5)
                await recepient.edit_folder(channel.entity.username, 1)
            if channel.pinned:
                await asyncio.sleep(2.5)
                await recepient(messages.ToggleDialogPinRequest(
                    channel.entity.username,
                    True
                ))
            ui.value = i
    except errors.FloodWaitError as flood:
        logger.warning(flood)
        ui.cooldown(flood)
        await asyncio.sleep(flood.seconds)
        ui.uncooldown()

    except Exception as e:
        logger.error(e)
        ui.unsuccess(e)
        return
    ui.success()