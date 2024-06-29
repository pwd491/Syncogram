import asyncio

from telethon import errors
from telethon.tl.functions import messages, account
from telethon.tl import types

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_secure_settings(ui: Task, **kwargs):
    """The algorithm for synchronizing security settings."""
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    ui.progress_counters.visible = True
    ui.total = 3
    timeout = .5

    while True:
        try:
            await asyncio.sleep(timeout)
            content: types.account.ContentSettings = await sender(
                account.GetContentSettingsRequest()
            )
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            timeout += 5
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    if content.sensitive_can_change:
        while True:
            try:
                await asyncio.sleep(timeout)
                await recepient(
                    account.SetContentSettingsRequest(content.sensitive_enabled)
                )
                ui.value += 1
                break
            except errors.SensitiveChangeForbiddenError as error:
                logger.error(error)
                ui.message(error, True)
            except errors.FloodWaitError as flood:
                logger.warning(flood)
                ui.message(flood)
                ui.cooldown(flood)
                timeout += 5
                await asyncio.sleep(flood.seconds)
                ui.uncooldown()

    while True:
        try:
            await asyncio.sleep(timeout)
            history: types.DefaultHistoryTTL = await sender(
                messages.GetDefaultHistoryTTLRequest()
            )
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            timeout += 5
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            await asyncio.sleep(timeout)
            await recepient(
                messages.SetDefaultHistoryTTLRequest(history.period)
            )
            ui.value += 1
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            timeout += 5
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            await asyncio.sleep(timeout)
            account_ttl: types.AccountDaysTTL = await sender(
                account.GetAccountTTLRequest()
            )
            break
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            timeout += 5
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    while True:
        try:
            await asyncio.sleep(timeout)
            await recepient(
                account.SetAccountTTLRequest(
                    types.TypeAccountDaysTTL(account_ttl.days)
                )
            )
            ui.value += 1
            break
        except errors.TtlDaysInvalidError as error:
            logger.error(error)
            ui.message(error, True)
        except errors.FloodWaitError as flood:
            logger.warning(flood)
            ui.message(flood)
            ui.cooldown(flood)
            timeout += 5
            await asyncio.sleep(flood.seconds)
            ui.uncooldown()

    ui.success()
