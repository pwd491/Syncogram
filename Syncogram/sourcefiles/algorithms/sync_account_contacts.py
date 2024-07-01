import asyncio

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
async def sync_contacts(ui: Task, **kwargs) -> None:
    """The algorithm for synchronizing the contact list."""
    ui.default()
    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    while True:
        try:
            request: types.contacts.Contacts = await sender(
                contacts.GetContactsRequest(0)
            )
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    users: list[types.User] = request.users
    non_sync: list[str] = []

    for contact in users.copy():
        if not contact.username and not contact.usernames:
            users.remove(contact)
            non_sync.append(contact.first_name)

    length = len(users)
    timeout = 2.5 if length <= 20 else 5 if 20 < length <= 50 else 10
    ui.total = length
    ui.progress_counters.visible = True

    for contact in users:
        while True:
            try:
                await asyncio.sleep(timeout)
                await recepient(
                    contacts.AddContactRequest(
                        id=contact.username or contact.usernames[0].username,
                        first_name=contact.first_name or str(),
                        last_name=contact.last_name or str(),
                        phone=contact.phone or str(),
                        add_phone_privacy_exception=True
                    )
                )
                ui.value += 1
                break
            except errors.ContactNameEmptyError as error:
                logger.error(error)
                ui.message(error, True)
                break
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.message(flood)
                ui.cooldown(flood)
                timeout += 5
                await asyncio.sleep(flood.seconds)
                ui.uncooldown()
    if non_sync:
        ui.message(f"Contacts was not sync: {non_sync}")

    ui.success()
