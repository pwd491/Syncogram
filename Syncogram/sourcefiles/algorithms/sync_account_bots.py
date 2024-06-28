import asyncio

from telethon import errors
from telethon.tl import types
from telethon.tl import custom
from telethon.tl.functions import account

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

    while True:
        try:
            source: list[custom.dialog.Dialog] = await sender.get_dialogs()
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

    bots: list[custom.dialog.Dialog] = []
    for dialog in source:
        if isinstance(dialog.entity, types.User):
            if dialog.entity.bot:
                if dialog.entity.username != "replies":
                    bots.append(dialog)

    ui.progress_counters.visible = True
    ui.total = len(bots) - 1

    timeout = 5 if ui.total < 50 else 10
    timeout_additional = 2.5

    bot: custom.dialog.Dialog
    for bot in bots:
        entity: types.User = bot.entity
        dialog: types.Dialog = bot.dialog
        while True:
            try:
                await asyncio.sleep(timeout)
                await recepient.send_message(entity.username, "/start")
                break
            except (errors.YouBlockedUserError, errors.UserIsBlockedError) as error:
                logger.error(error)
                ui.message(f"Unable to sync: @{entity.username}", True)
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.cooldown(flood)
                timeout += 5
                asyncio.sleep(flood.seconds)
                ui.uncooldown()
        
        while True:
            try:
                await asyncio.sleep(timeout_additional)
                await recepient(account.UpdateNotifySettingsRequest(
                    peer=entity.username,
                    settings=types.InputPeerNotifySettings(
                        show_previews=dialog.notify_settings.show_previews,
                        mute_until=dialog.notify_settings.mute_until,
                        sound=types.NotificationSoundDefault(),
                        stories_muted=dialog.notify_settings.stories_muted,
                        stories_hide_sender=dialog.notify_settings.stories_hide_sender,
                        stories_sound=types.NotificationSoundDefault()
                    )
                ))
                break
            except errors.PeerIdInvalidError as error:
                logger.warning(error)
                ui.message(f"Failed to synchronize notification settings for: @{entity.username}", True)
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.message(flood)
                ui.cooldown(flood)
                timeout_additional += 5
                await asyncio.sleep(flood.seconds)
                ui.uncooldown()
        ui.value += 1
    ui.success()
