import asyncio
from typing import Any

from telethon import errors
from telethon.tl import types
from telethon.tl.functions import contacts

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_blacklist(ui: Task, **kwargs):
    """The algorithm for synchronizing blacklist."""
    async def get_blocked(client: UserClient) -> list[types.User]:
        source: list[types.User] = []
        while True:
            try:
                request: types.contacts.Blocked | types.contacts.BlockedSlice = \
                    await client(
                        contacts.GetBlockedRequest(
                            offset=0,
                            limit=1_000_000,
                            my_stories_from=False
                        )
                    )
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.cooldown(flood)
                ui.message(flood)
                asyncio.sleep(flood.seconds)
                ui.uncooldown()
        source.extend(request.users)
        return source

    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    sender_blacklist: list[types.User] = await get_blocked(sender)
    recepient_blacklist: list[types.User] = await get_blocked(recepient)

    blocked: types.User
    for blocked in sender_blacklist.copy():
        if not (blocked.username or blocked.usernames):
            sender_blacklist.remove(blocked)
        else:
            for r_blocked in recepient_blacklist.copy():
                if blocked.id == r_blocked.id:
                    sender_blacklist.remove(blocked)
                    recepient_blacklist.remove(r_blocked)
                    break

    length = len(sender_blacklist)
    if length <= 20:
        timeout = 2.5
    elif 20 <= length <= 50:
        timeout = 5
    else:
        timeout = 10

    ui.total = length
    ui.progress_counters.visible = True

    for blocked in sender_blacklist:
        while True:
            try:
                await asyncio.sleep(timeout)
                await recepient(
                    contacts.BlockRequest(
                        id=blocked.username or blocked.usernames[0].username,
                        my_stories_from=False
                    )
                )
                break
            except errors.ContactIdInvalidError as error:
                logger.error(error)
                ui.message(
                    f"Can't sync: @{
                        blocked.username or blocked.usernames[0].username
                        }", True
                )
                break
            except (errors.FloodWaitError) as flood:
                logger.warning(flood)
                ui.cooldown(flood)
                ui.message(flood)
                timeout += 5
                asyncio.sleep(flood.seconds)
                ui.uncooldown()

        ui.value += 1
    ui.success()
