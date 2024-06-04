import asyncio
from datetime import datetime
from typing import Callable, Coroutine

import flet as ft
from telethon import events
from telethon import errors
from telethon.tl import types
from telethon.tl.functions import users
from telethon.tl.functions import photos
from telethon.tl.functions import account
from telethon.tl.functions import channels
from telethon.tl.functions import messages
from telethon.tl.custom.dialog import Dialog
from telethon.tl.patched import MessageService

from ..telegram import UserClient
from ..database import SQLite
from ..components import Task


class Manager:
    """The manager to control options UI and Coroutines."""
    def __init__(self, page: ft.Page, _) -> None:
        self.page: ft.Page = page
        self.database = SQLite()
        self.client = UserClient

        self.options = {
            "is_sync_fav": {
                "title": _("Synchronize my favorite messages between accounts."),
                "description": _(
                    "Sync messages in your favorite chat with the correct sequence, re-replies to messages and pinned messages. The program can synchronize up to 100 messages per clock cycle."
                ),
                "function": self.sync_favorite_messages,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_profile_name": {
                "title": _(
                    "Synchronize the first name, last name, biography and birthday of the profile."
                ),
                "description": _(
                    "Synchronization of the first name, last name, profile description and birthday. If you do not specify the data, it will be overwritten as empty fields."
                ),
                "function": self.sync_profile_first_name_and_second_name,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_profile_avatars": {
                "title": _("Synchronize account photos and videos avatars."),
                "description": _(
                    "Sync photo and video avatars in the correct sequence. If there are a lot of media files, the program sets an average limit between requests to the servers in order to circumvent the restrictions."
                ),
                "function": self.sync_profile_avatars,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_public_channels_and_groups": {
                "title": _("Synchronize public channels and groups."),
                "description": _(
                    "Synchronizes public channels ang groups. If the channel or groups was archived or pinned, the program will save these parameters."
                ),
                "function": self.sync_public_channels_and_groups,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_privacy": {
                "title": _("Synchronize privacy settings."),
                "description": _(
                    "Synchronizes the privacy settings for the account. If the sync account does not have Telegram Premium, then the corresponding premium settings will not be synchronized."
                ),
                "function": self.sync_privacy_settings,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_secure": {
                "title": _("Synchronize secure settings."),
                "description": _(
                    "Synchronizes the secure settings for the account. It includes synchronization of sensitive content, TTL messages and account."
                ),
                "function": self.sync_secure_settings,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_stickers_emojis_gifs": {
                "title": _("Synchronize stickers, emojis and gifs."),
                "description": _(
                    "Synchronizes the stickers sets, emojis and saved gifs. It also enables automatic transfer of archived stickers or emojis, and faved stickers."
                ),
                "function": self.sync_stickers_emojis_gifs,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_bots": {
                "title": _("Synchronize bots."),
                "description": _(
                    "Synchronizes the list of bots. Attention, this function does not transfer the message history."
                ),
                "function": self.sync_bots,
                "status": bool(False),
                "ui": Task,
            },
        }
        self.callback()

    def update_options_dict(self):
        """Get options list and update dict variable."""
        list_of_options = self.database.get_options()
        if list_of_options is None:
            return
        list_of_options = list_of_options[1:]

        for n, option in enumerate(self.options.items()):
            option[1].update({"status": bool(list_of_options[n])})

        for option in self.options.items():
            if option[1].get("status"):
                title = option[1].get("title")
                desc = option[1].get("description")
                option[1].update({"ui": Task(title, desc)})

    def get_ui_tasks(self) -> list[Task]:
        """Return UI list of will be execute tasks."""
        lst = []
        for option in self.options.items():
            if option[1].get("status"):
                lst.append(option[1].get("ui"))
        return lst

    def get_tasks_coroutines(self) -> list[Coroutine]:
        """Return coroutines objects."""
        lst = []
        for option in self.options.items():
            if option[1].get("status"):
                lst.append(option[1].get("function"))
        return lst

    def get_coroutines_with_ui(self) -> list[Callable[[Task], None]]:
        """Return dict object."""
        lst = []
        for option in self.options.items():
            if option[1].get("status"):
                func = option[1].get("function")
                ui = option[1].get("ui")
                lst.append(func(ui))
        return lst

    def callback(self):
        """Callback"""
        self.update_options_dict()

    async def sync_favorite_messages(self, ui: Task):
        """
        An algorithm for forwarding messages to the recipient entity is
        implemented.
        """
        ui.default()
        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        sender_username = self.database.get_username_by_status(1)
        recepient_username = self.database.get_username_by_status(0)

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        sender_entity = await recepient.get_input_entity(sender_username)
        recepient_entity = await sender.get_input_entity(recepient_username)

        # Getting messages from sender source
        source_messages = await sender.get_messages(
            sender_entity, min_id=0, max_id=0, reverse=True
        )

        is_grouped_id = None
        is_pinned = False
        is_replied = False
        group = []
        msg_ids = {}

        async def recepient_save_message(
            message_id,
            message_length,
            is_pin: bool,
            is_reply: None | types.Message
        ):
            data = await recepient.get_messages(
                sender_entity,
                limit=message_length
            )
            messages: list[types.Message] = list(data)
            if is_reply:
                destination_message_id = msg_ids.get(is_reply.reply_to_msg_id)
                if messages[0].media:
                    await asyncio.sleep(3)
                    message = await recepient.send_message(
                        recepient_entity,
                        messages[-1].message,
                        file=messages,
                        reply_to=destination_message_id,
                    )
                    msg_ids[message_id] = message[0].id
                else:
                    await asyncio.sleep(3)
                    message = await recepient.send_message(
                        recepient_entity,
                        message=messages[0],
                        reply_to=destination_message_id,
                    )
                    msg_ids[message_id] = message.id
            else:
                message = await recepient.forward_messages(recepient_entity, messages)
                msg_ids[message_id] = message[0].id

            if is_pin:
                await asyncio.sleep(3)
                await recepient.pin_message(recepient_entity, message[0])
            await asyncio.sleep(3)
            await recepient.delete_messages(sender_entity, messages)

        try:
            ui.progress_counters.visible = True
            ui.total = source_messages.total
            message: types.Message
            for i, message in enumerate(source_messages, 1):
                ui.value = i
                if not isinstance(message, MessageService):
                    if message.grouped_id is not None:
                        if message.pinned:
                            is_pinned = True
                        if message.reply_to:
                            is_replied = message.reply_to
                        if is_grouped_id != message.grouped_id:
                            is_grouped_id = message.grouped_id
                            if group:
                                await asyncio.sleep(3)
                                await sender.forward_messages(
                                    recepient_entity, group, silent=True
                                )
                                await recepient_save_message(
                                    message.id, len(group), is_pinned, is_replied
                                )
                                is_pinned = False
                                is_replied = False
                                group.clear()
                        group.append(message)
                        continue
                    if group:
                        await asyncio.sleep(3)
                        await sender.forward_messages(
                            recepient_entity, group, silent=True
                        )
                        await recepient_save_message(
                            message.id, len(group), is_pinned, is_replied
                        )
                        is_pinned = False
                        is_replied = False
                        group.clear()

                    await asyncio.sleep(3)
                    await sender.forward_messages(
                        recepient_entity, message, silent=True
                    )
                    await recepient_save_message(
                        message.id, 1, message.pinned, message.reply_to
                    )

            if group:
                await asyncio.sleep(3)
                await sender.forward_messages(recepient_entity, group, silent=True)
                await recepient_save_message(
                    group[-1].id, len(group), is_pinned, is_replied
                )
                is_pinned = False
                is_replied = False
                group.clear()
        except Exception as e:
            ui.unsuccess(e)
            return
        ui.success()

    async def sync_profile_first_name_and_second_name(self, ui: Task):
        """
        Connecting accounts, getting profile data and sets.
        """
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        ui.progress_counters.visible = True
        ui.total = 4
        try:
            user = await sender(
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
            ui.unsuccess(e)
            return
        ui.success()

    async def sync_profile_avatars(self, ui: Task):
        """
        The algorithm for synchronizing profile photo and video avatars to 
        the recipient's essence.
        """
        ui.default()
        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        image_extension = ".jpeg"
        video_extension = ".mp4"
        photo: types.Photo
        try:
            avatars = await sender.get_profile_photos("me")
            user: types.users.UserFull = await sender(
                users.GetFullUserRequest('me')
            )
            fallback = user.full_user.fallback_photo

            ui.progress_counters.visible = True
            ui.total = avatars.total
            for i, photo in enumerate(reversed(avatars), 1):
                await asyncio.sleep(3)
                blob = await sender.download_media(photo, bytes)
                name = "Syncogram_" + datetime.strftime(
                    photo.date, "%Y_%m_%d_%H_%M_%S"
                )

                await recepient(
                    photos.UploadProfilePhotoRequest(
                        file=await recepient.upload_file(
                            blob,
                            file_name=name + image_extension
                        ) if not photo.video_sizes else None,
                        video=await recepient.upload_file(
                            blob,
                            file_name=name + video_extension
                        ) if photo.video_sizes else None
                    )
                )
                ui.value = i

            if fallback:
                blob = await sender.download_media(fallback, bytes)
                name = "Syncogram_" + datetime.strftime(
                    photo.date, "%Y_%m_%d_%H_%M_%S"
                )

                await recepient(
                    photos.UploadProfilePhotoRequest(
                        fallback=True,
                        file=await recepient.upload_file(
                            blob,
                            file_name=name + image_extension
                        ) if not fallback.video_sizes else None,
                        video=await recepient.upload_file(
                            blob,
                            file_name=name + video_extension
                        ) if fallback.video_sizes else None
                    )
                )

        except Exception as e:
            ui.unsuccess(e)
            return
        ui.success()

    async def sync_public_channels_and_groups(self, ui: Task):
        """
        The algorithm for synchronizing public channels, 
        the status of pinning and archiving.
        """
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        source = await sender.get_dialogs()
        channels_list: list[Dialog] = []

        dialog: Dialog
        for dialog in source:
            if not isinstance(dialog.entity, types.Chat) \
                and not dialog.is_user \
                    and dialog.entity.username:
                channels_list.append(dialog)

        ui.progress_counters.visible = True
        ui.total = len(channels_list)

        channel: Dialog
        try:
            for i, channel in enumerate(channels_list, 1):
                await asyncio.sleep(12)
                await recepient(
                    channels.JoinChannelRequest(channel.entity.username)
                )
                if channel.archived:
                    await asyncio.sleep(2.5)
                    await recepient.edit_folder(channel.entity.username, 1)
                if channel.pinned:
                    await asyncio.sleep(2.5)
                    await recepient(messages.ToggleDialogPinRequest(
                        channel.entity.username,
                        True
                    ))
                ui.value = i
        except Exception as e:
            ui.unsuccess(e)
            return
        ui.success()


    async def sync_privacy_settings(self, ui: Task):
        """The algorithm for synchronizing privacy settings."""
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not sender.is_connected() or not recepient.is_connected():
            await sender.connect()
            await recepient.connect()

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

        try:
            ui.progress_counters.visible = True
            ui.total = len(input_privacies) + 1
            i: int
            for i, privacy in enumerate(input_privacies, 1):
                await asyncio.sleep(1)
                rules: list[types.TypePrivacyRule] = []
                request: types.account.PrivacyRules = await sender(
                    account.GetPrivacyRequest(
                        privacy
                    )
                )

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

                await recepient(
                    account.SetPrivacyRequest(
                        key=privacy,
                        rules=rules
                    )
                )
                ui.value = i

            data: types.TypeGlobalPrivacySettings = await sender(
                account.GetGlobalPrivacySettingsRequest()
            )

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
            ui.value = i + 1
        except Exception as e:
            ui.unsuccess(e)
            return

        ui.success()

    async def sync_secure_settings(self, ui: Task):
        """The algorithm for synchronizing security settings."""
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not sender.is_connected() or not recepient.is_connected():
            await sender.connect()
            await recepient.connect()

        ui.progress_counters.visible = True
        ui.total = 3
        try:
            request: types.account.ContentSettings = await sender(
                account.GetContentSettingsRequest()
            )
            await asyncio.sleep(0.5)
            if request.sensitive_can_change:
                await recepient(
                    account.SetContentSettingsRequest(request.sensitive_enabled)
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
            ui.unsuccess(e)
            return
        ui.success()

    async def sync_stickers_emojis_gifs(self, ui: Task):
        """The algorithm for synchronizing stickers and other things."""
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not sender.is_connected() or not recepient.is_connected():
            await sender.connect()
            await recepient.connect()

        s_entity: types.User = await sender.get_entity('me')
        r_entity: types.User = await recepient.get_entity('me')

        timeout = 5

        @recepient.on(events.NewMessage(
            from_users=[s_entity.username], func=lambda e: e.message.gif)
        )
        async def gifhook(event: events.NewMessage.Event):
            gif: types.Document = event.message.gif
            try:
                await recepient(
                    messages.SaveGifRequest(
                        types.InputDocument(
                            gif.id,
                            gif.access_hash,
                            gif.file_reference
                        ),
                        unsave=False
                    )
                )
            except Exception as e:
                print(e)

        faved_stickers_list: types.messages.FavedStickers = await sender(
            messages.GetFavedStickersRequest(0)
        )
        faved_stickers: list[types.Document] = faved_stickers_list.stickers

        stickers_list: types.messages.AllStickers = await sender(
            messages.GetAllStickersRequest(0)
        )
        stickers: list[types.TypeStickerSet] = stickers_list.sets

        stickers_archived_list: types.messages.ArchivedStickers = await sender(
            messages.GetArchivedStickersRequest(
                offset_id=0,
                limit=0,
                masks=False,
                emojis=False
            )
        )
        stickers_archived: list[types.StickerSetCovered] = stickers_archived_list.sets

        emojis_list: types.messages.AllStickers = await sender(
            messages.GetEmojiStickersRequest(0)
        )
        emojis: list[types.TypeStickerSet] = emojis_list.sets

        emojis_archived_list: types.messages.ArchivedStickers = await sender(
            messages.GetArchivedStickersRequest(
                offset_id=0,
                limit=0,
                masks=False,
                emojis=True
            )
        )

        emojis_archived: list[types.StickerSetFullCovered] = emojis_archived_list.sets

        gifs_list: types.messages.SavedGifs = await sender(
            messages.GetSavedGifsRequest(0)
        )
        gifs: list[types.TypeDocument] = gifs_list.gifs

        ui.progress_counters.visible = True
        ui.total = len(faved_stickers) + len(stickers) + len(stickers_archived) \
              + len(emojis) + len(emojis_archived) + len(gifs)

        ui.value = 0
        if faved_stickers:
            for sticker in reversed(faved_stickers):
                await asyncio.sleep(timeout)
                try:
                    await recepient(
                        messages.FaveStickerRequest(
                            id=types.InputDocument(
                                id=sticker.id,
                                access_hash=sticker.access_hash,
                                file_reference=sticker.file_reference
                            ),
                            unfave=False
                        )
                    )
                    ui.value += 1
                except errors.StickerIdInvalidError:
                    continue

        if stickers:
            for sticker in reversed(stickers):
                await asyncio.sleep(timeout)
                try:
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                sticker.short_name
                            ),
                            archived=False
                        )
                    )
                    ui.value += 1
                except errors.StickersetInvalidError:
                    continue

        if stickers_archived:
            for sticker in reversed(stickers_archived):
                await asyncio.sleep(timeout)
                try:
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                sticker.set.short_name
                            ),
                            archived=True
                        )
                    )
                    ui.value += 1
                except errors.StickersetInvalidError:
                    continue

        if emojis:
            for emoji in reversed(emojis):
                await asyncio.sleep(timeout)
                try:
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                emoji.short_name
                            ),
                            archived=False
                        )
                    )
                    ui.value += 1
                except errors.StickersetInvalidError:
                    continue

        if emojis_archived:
            for emoji in reversed(emojis_archived):
                await asyncio.sleep(timeout)
                try:
                    await recepient(
                        messages.InstallStickerSetRequest(
                            stickerset=types.InputStickerSetShortName(
                                emoji.set.short_name
                            ),
                            archived=True
                        )
                    )
                    ui.value += 1
                except errors.StickersetInvalidError:
                    continue


        will_delete = []
        if gifs:
            for gif in reversed(gifs):
                await asyncio.sleep(timeout)
                try:
                    message = await sender.send_file(r_entity.username, gif)
                    will_delete.append(message)
                    ui.value += 1
                except Exception:
                    continue

        if will_delete:
            try:
                await sender.delete_messages(r_entity.username, will_delete)
            except errors.MessageDeleteForbiddenError:
                pass

        ui.success()


    async def sync_bots(self, ui: Task):
        ui.default()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not sender.is_connected() or not recepient.is_connected():
            await sender.connect()
            await recepient.connect()

        dialogs: list[Dialog] = await sender.get_dialogs()

        bots: list[types.User] = []
        dialog: Dialog
        for dialog in dialogs:
            if isinstance(dialog.entity, types.User):
                if dialog.entity.bot:
                    bots.append(dialog.entity)

        ui.progress_counters.visible = True
        ui.total = len(bots) - 1
        for bot in bots:
            await asyncio.sleep(5)
            try:
                await recepient.send_message(bot.username, "/start")
                ui.value += 1
            except (errors.YouBlockedUserError, errors.UserIsBlockedError):
                pass

        ui.success()
