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
async def sync_bots(ui: Task, **kwargs) -> None:
    """The algorithm for synchronizing bots in telegram."""
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    try:
        dialogs: list[Dialog] = await sender.get_dialogs()
    except (
        errors.InputConstructorInvalidError,
        errors.OffsetPeerIdInvalidError,
        errors.SessionPasswordNeededError,
        errors.TimeoutError
    ) as error:
        logger.critical(error)
        ui.unsuccess(error)
        return
    except errors.FloodWaitError as flood:
        logger.warning(flood)
        ui.cooldown(flood)
        asyncio.sleep(flood.seconds)
        ui.uncooldown()
        dialogs: list[Dialog] = await sender.get_dialogs()

    bots: list[types.User] = []
    dialog: Dialog
    for dialog in dialogs:
        if isinstance(dialog.entity, types.User):
            if dialog.entity.bot:
                bots.append(dialog.entity)

    ui.progress_counters.visible = True
    ui.total = len(bots) - 1

    timeout = 5 if ui.total < 50 else 10

    bot: types.User
    for bot in bots:
        await asyncio.sleep(timeout)
        try:
            await recepient.send_message(bot.username, "/start")
            ui.value += 1
        except (errors.YouBlockedUserError, errors.UserIsBlockedError) as error:
            logger.error(error)
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            timeout += 5
            asyncio.sleep(flood.seconds)
            ui.uncooldown()
            await recepient.send_message(bot.username, "/start")
            ui.value += 1
    ui.success()
