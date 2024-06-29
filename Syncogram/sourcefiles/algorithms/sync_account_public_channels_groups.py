import datetime
import asyncio

from telethon import errors
from telethon.tl.functions import channels, messages, account
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
    The algorithm for synchronizing public channels and groups, 
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

    while True:
        try:
            source: list[Dialog] = await sender.get_dialogs()
            break
        except (
            errors.InputConstructorInvalidError,
            errors.OffsetPeerIdInvalidError,
            errors.SessionPasswordNeededError,
            errors.TimeoutError
        ) as error:
            logger.critical(error)
            ui.unsuccess("It is not possible to get a list of the sender's channels.")
            ui.message("It is not possible to get a list of the sender's channels.")
            return
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            recepient_channels: list[Dialog] = await sender.get_dialogs()
            break
        except (
            errors.InputConstructorInvalidError,
            errors.OffsetPeerIdInvalidError,
            errors.SessionPasswordNeededError,
            errors.TimeoutError
        ) as error:
            logger.critical(error)
            ui.unsuccess("It is not possible to get a list of the recepient's channels.")
            ui.message("It is not possible to get a list of the recepient's channels.")
            return
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            asyncio.sleep(flood.seconds)
            ui.uncooldown()

    channels_list: list[Dialog] = get_public_channels(source)
    recepient_channels: list[Dialog] = get_public_channels(recepient_channels)
    r_channels: list[int] = [channel.entity.id for channel in recepient_channels]

    ui.progress_counters.visible = True
    ui.total = len(channels_list)

    timeout = 10 if len(channels_list) <= 50 else 20
    timeout_additional = 2.5

    channel: Dialog
    for channel in channels_list:
        entity: types.Channel = channel.entity
        if entity.id not in r_channels:
            while True:
                try:
                    await asyncio.sleep(timeout)
                    await recepient(
                        channels.JoinChannelRequest(entity.username)
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
                    ui.message(f"Unsuccess join to: @{entity.title}", True)
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

            dialog: types.Dialog = channel.dialog
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

            if channel.archived:
                while True:
                    try:
                        await asyncio.sleep(timeout_additional)
                        await recepient.edit_folder(entity.username, 1)
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood)
                        ui.cooldown(flood)
                        timeout_additional += 5
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()

            if channel.pinned:
                while True:
                    try:
                        await asyncio.sleep(timeout_additional)
                        await recepient(messages.ToggleDialogPinRequest(
                            entity.username,
                            True
                        ))
                        break
                    except errors.FloodWaitError as flood:
                        logger.warning(flood)
                        ui.message(flood, True)
                        ui.cooldown(flood)
                        timeout_additional += 5
                        await asyncio.sleep(flood.seconds)
                        ui.uncooldown()
        ui.value += 1

    ui.success()
