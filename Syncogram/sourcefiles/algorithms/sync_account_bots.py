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

    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    sender_dialogs: list[custom.dialog.Dialog] = await __get_dialogs(sender)
    if sender_dialogs is None:
        return
    recepient_dialogs: list[custom.dialog.Dialog] = await __get_dialogs(recepient)

    s_dialog: custom.dialog.Dialog
    for s_dialog in sender_dialogs.copy():
        if not isinstance(s_dialog.entity, types.User):
            sender_dialogs.remove(s_dialog)
        elif not s_dialog.entity.bot:
            sender_dialogs.remove(s_dialog)
        elif s_dialog.entity.username == "replies":
            sender_dialogs.remove(s_dialog)
        else:
            if recepient_dialogs is not None:
                for r_dialog in recepient_dialogs:
                    if s_dialog.entity.id == r_dialog.entity.id:
                        sender_dialogs.remove(s_dialog)

    ui.progress_counters.visible = True
    ui.total = len(sender_dialogs)

    timeout = 5 if ui.total < 50 else 10
    timeout_additional = 2.5

    bot: custom.dialog.Dialog
    for bot in sender_dialogs:
        entity: types.User = bot.entity
        dialog: types.Dialog = bot.dialog
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
                ui.message(f"Failed to sync notification settings for: @{entity.username or entity.usernames[0].username}", True)
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.message(flood)
                ui.cooldown(flood)
                timeout_additional += 5
                await asyncio.sleep(flood.seconds)
                ui.uncooldown()

        while True:
            try:
                await asyncio.sleep(timeout)
                await recepient.send_message(entity.username, "/start")
                ui.value += 1
                break
            except (errors.YouBlockedUserError, errors.UserIsBlockedError) as error:
                logger.error(error)
                ui.message(f"Unable to sync: @{entity.username or entity.usernames[0].username}", True)
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.cooldown(flood)
                timeout += 5
                asyncio.sleep(flood.seconds)
                ui.uncooldown()

    ui.success()
