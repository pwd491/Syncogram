import asyncio

from telethon import errors
from telethon.tl.functions import users, account
from telethon.tl import types

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_profile_first_name_and_second_name(ui: Task, **kwargs):
    """
    The algorithm for syncing avatar photos/stickers, avatar videos and
    fallback photo.
    """
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    try:
        user: types.users.UserFull = await sender(
            users.GetFullUserRequest("me")
        )
    except (errors.TimedOutError, errors.UserIdInvalidError) as error:
        logger.critical(error)
        ui.unsuccess(error)
        return

    timeout = 1
    ui.total = 4 if user.full_user.birthday else 3
    ui.progress_counters.visible = True

    first_name = user.users[0].first_name
    first_name = str() if first_name is None else first_name

    last_name = user.users[0].last_name
    last_name = str() if last_name is None else last_name

    bio = user.full_user.about
    bio = str() if bio is None else bio

    try:
        await asyncio.sleep(timeout)
        await recepient(
            account.UpdateProfileRequest(first_name, last_name, bio)
        )
        ui.value += 3
    except (errors.AboutTooLongError, errors.FirstNameInvalidError) as error:
        logger.warning(error)
    except errors.FloodWaitError as flood:
        logger.warning(flood)
        ui.cooldown(flood)
        await asyncio.sleep(flood.seconds)
        ui.uncooldown()
        await recepient(
            account.UpdateProfileRequest(first_name, last_name, bio)
        )
        ui.value += 3

    if user.full_user.birthday is not None:
        try:
            await recepient(
                account.UpdateBirthdayRequest(
                    types.TypeBirthday(
                        user.full_user.birthday.day,
                        user.full_user.birthday.month,
                        user.full_user.birthday.year
                    )
                )
            )
            ui.value += 1

        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()
            await recepient(
                account.UpdateBirthdayRequest(
                    types.TypeBirthday(
                        user.full_user.birthday.day,
                        user.full_user.birthday.month,
                        user.full_user.birthday.year
                    )
                )
            )
            ui.value += 1

    ui.success()
