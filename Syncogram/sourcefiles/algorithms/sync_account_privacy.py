import asyncio

from telethon import errors
from telethon.tl.functions import account
from telethon.tl import types

from .decorators import autoconnect
from ..components import Task
from ..telegram import UserClient
from ..utils import logging

logger = logging()

@logger.catch()
@autoconnect
async def sync_privacy_settings(ui: Task, **kwargs):
    """The algorithm for synchronizing privacy settings."""
    ui.default()

    sender: UserClient = kwargs["sender"]
    recepient: UserClient = kwargs["recepient"]

    input_privacies: list[types.TypeInputPrivacyKey] = [
        types.InputPrivacyKeyPhoneNumber(),
        types.InputPrivacyKeyAddedByPhone(),
        types.InputPrivacyKeyStatusTimestamp(),
        types.InputPrivacyKeyProfilePhoto(),
        types.InputPrivacyKeyAbout(),
        types.InputPrivacyKeyBirthday(),
        types.InputPrivacyKeyForwards(),
        types.InputPrivacyKeyPhoneCall(),
        types.InputPrivacyKeyPhoneP2P(),
        types.InputPrivacyKeyChatInvite(),
        types.InputPrivacyKeyVoiceMessages(),
    ]

    ui.progress_counters.visible = True
    ui.total = len(input_privacies)
    timeout = 1

    for privacy in input_privacies:
        await asyncio.sleep(timeout)
        rules: list[types.TypePrivacyRule] = []
        while True:
            try:
                request: types.account.PrivacyRules = await sender(
                    account.GetPrivacyRequest(
                        privacy
                    )
                )
                break
            except errors.PrivacyKeyInvalidError as error:
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

        for rule in request.rules:
            if isinstance(rule, types.PrivacyValueAllowAll):
                rules.append(types.InputPrivacyValueAllowAll())

            if isinstance(rule, types.PrivacyValueAllowUsers):
                rules.append(types.InputPrivacyValueAllowUsers([]))

            if isinstance(rule, types.PrivacyValueAllowPremium):
                rules.append(types.InputPrivacyValueAllowPremium())

            if isinstance(rule, types.PrivacyValueAllowContacts):
                rules.append(types.InputPrivacyValueAllowContacts())

            if isinstance(rule, types.PrivacyValueAllowCloseFriends):
                rules.append(types.InputPrivacyValueAllowCloseFriends())

            if isinstance(rule, types.PrivacyValueAllowChatParticipants):
                rules.append(types.InputPrivacyValueAllowChatParticipants([]))

            if isinstance(rule, types.PrivacyValueDisallowAll):
                r = True
                for k in rules:
                    if isinstance(k, types.InputPrivacyValueAllowContacts):
                        r = False
                        break
                if r:
                    rules.append(types.InputPrivacyValueDisallowAll())

            if isinstance(rule, types.PrivacyValueDisallowUsers):
                rules.append(types.InputPrivacyValueDisallowUsers([]))

            if isinstance(rule, types.PrivacyValueDisallowContacts):
                rules.append(types.InputPrivacyValueDisallowContacts())

            if isinstance(rule, types.PrivacyValueDisallowChatParticipants):
                rules.append(types.InputPrivacyValueDisallowChatParticipants([]))

        while True:
            try:
                await recepient(
                    account.SetPrivacyRequest(
                        key=privacy,
                        rules=rules
                    )
                )
                ui.value += 1
                break
            except (
                errors.PrivacyKeyInvalidError, errors.PrivacyTooLongError
            ) as error:
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

        while True:
            try:
                data: types.TypeGlobalPrivacySettings = await sender(
                    account.GetGlobalPrivacySettingsRequest()
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
                await recepient(
                    account.SetGlobalPrivacySettingsRequest(
                        types.TypeGlobalPrivacySettings(
                            data.archive_and_mute_new_noncontact_peers,
                            data.keep_archived_unmuted,
                            data.keep_archived_folders,
                            data.hide_read_marks,
                            data.new_noncontact_peers_require_premium
                        )
                    )
                )
                ui.value += 1
                break
            except errors.AutoarchiveNotAvailableError as error:
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
    ui.success()
