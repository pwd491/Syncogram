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

    try:
        content: types.account.ContentSettings = await sender(
            account.GetContentSettingsRequest()
        )
        await asyncio.sleep(0.5)
        if content.sensitive_can_change:
            await recepient(
                account.SetContentSettingsRequest(content.sensitive_enabled)
            )
        ui.value += 1
        await asyncio.sleep(0.5)

        request: types.DefaultHistoryTTL = await sender(
            messages.GetDefaultHistoryTTLRequest()
        )
        await asyncio.sleep(0.5)
        await recepient(
            messages.SetDefaultHistoryTTLRequest(request.period)
        )
        ui.value += 1
        await asyncio.sleep(0.5)

        request: types.AccountDaysTTL = await sender(
            account.GetAccountTTLRequest()
        )
        await asyncio.sleep(0.5)
        await recepient(
            account.SetAccountTTLRequest(
                types.TypeAccountDaysTTL(request.days)
            )
        )
        ui.value += 1
        await asyncio.sleep(0.5)

    except Exception as e:
        logger.error(e)
        ui.unsuccess(e)
        return
    ui.success()