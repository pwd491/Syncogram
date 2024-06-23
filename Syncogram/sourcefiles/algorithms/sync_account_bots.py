import asyncio

from telethon import errors
from telethon.tl import types
from telethon.tl.custom.dialog import Dialog

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_bots(ui: Task, **kwargs):
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    dialogs: list[Dialog] = await sender.get_dialogs()

    bots: list[types.User] = []
    dialog: Dialog
    for dialog in dialogs:
        if isinstance(dialog.entity, types.User):
            if dialog.entity.bot:
                bots.append(dialog.entity)

    ui.progress_counters.visible = True
    ui.total = len(bots) - 1
    bot: types.User
    for bot in bots:
        await asyncio.sleep(5)
        try:
            await recepient.send_message(bot.username, "/start")
            ui.value += 1
        except (errors.YouBlockedUserError, errors.UserIsBlockedError) as e:
            logger.error(e)
    ui.success()
