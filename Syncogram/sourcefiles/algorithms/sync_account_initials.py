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
    Connecting accounts, getting profile data and sets.
    """
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    ui.progress_counters.visible = True
    ui.total = 4
    try:
        user: types.users.UserFull = await sender(
            users.GetFullUserRequest("me")
        )

        ui.value += 1
        await asyncio.sleep(1)
        first_name = user.users[0].first_name
        first_name = str() if first_name is None else first_name
        await asyncio.sleep(1)

        last_name = user.users[0].last_name
        last_name = str() if last_name is None else last_name
        ui.value += 1
        await asyncio.sleep(1)

        bio = user.full_user.about
        bio = str() if bio is None else bio
        ui.value += 1
        await asyncio.sleep(1)

        await recepient(
            account.UpdateProfileRequest(first_name, last_name, bio)
        )
        await asyncio.sleep(1)

        if user.full_user.birthday is not None:
            await recepient(
                account.UpdateBirthdayRequest(
                    types.TypeBirthday(
                        user.full_user.birthday.day,
                        user.full_user.birthday.month,
                        user.full_user.birthday.year
                    )
                )
            )
        await asyncio.sleep(1)
        ui.value += 1

    except Exception as e:
        logger.error(e)
        ui.unsuccess(e)
        return
    ui.success()