import asyncio
from datetime import datetime
from typing import Callable, Coroutine

import flet as ft
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.patched import MessageService
from telethon.tl.types import UserFull, Message, Photo
from telethon.tl.functions.photos import (UploadProfilePhotoRequest)

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
                "title": _("Sync my favorite messages between accounts."),
                "description": _("Sync messages in your favorite chat with the correct sequence, re-replies to messages and pinned messages. The program can synchronize up to 100 messages per clock cycle."),
                "function": self.sync_favorite_messages,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_profile_name": {
                "title": _(
                    "Synchronize the first name, last name and biography of the profile."
                ),
                "description": _("Synchronization of the first name, last name and profile description. If you do not specify the data, it will be overwritten as empty fields."),
                "function": self.sync_profile_first_name_and_second_name,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_profile_media": {
                "title": _(
                    "Synchronize account photos and videos avatars."
                ),
                "description": _("Sync photo and video avatars in the correct sequence. If there are a lot of media files, the program sets an average limit between requests to the servers in order to circumvent the restrictions."),
                "function": self.sync_profile_media,
                "status": bool(False),
                "ui": Task,
            },
            "is_sync_public_channels": {
                "title": _(
                    "Sync public channels."
                ),
                "description": _("Synchronizes public channels. If the channel was archived or pinned, the program will save these parameters."),
                "function": self.sync_public_channels,
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
        source_messages = sender.iter_messages(
            sender_entity, min_id=0, max_id=0, reverse=True
        )

        is_grouped_id = None
        is_pinned = False
        is_replied = False
        group = []
        msg_ids = {}

        async def recepient_save_message(
            message_id, message_length, is_pin: bool, is_reply: None | Message
        ):
            data = await recepient.get_messages(sender_entity, limit=message_length)
            messages = [message for message in data]
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
            i = 0
            async for message in source_messages:
                i += 1
                ui.total.value = source_messages.total
                ui.progress.value = i / source_messages.total
                ui.value.value = i
                ui.update()
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
            return ui.unsuccess(e)
        finally:
            del msg_ids
            sender.disconnect()
            recepient.disconnect()

        ui.success()

    async def sync_profile_first_name_and_second_name(self, ui: Task):
        """
        Connecting accounts, getting profile data and sets.
        """
        ui.progress.value = None
        ui.progress.update()

        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        try:
            user: UserFull = await sender(GetFullUserRequest("me"))
            first_name = user.users[0].first_name
            first_name = "" if first_name is None else first_name
            last_name = user.users[0].last_name
            last_name = "" if last_name is None else last_name
            bio = user.full_user.about
            bio = "" if bio is None else bio

            await recepient(UpdateProfileRequest(first_name, last_name, bio))
        except Exception as e:
            return ui.unsuccess(e)
        finally:
            sender.disconnect()
            recepient.disconnect()

        ui.success()


    async def sync_profile_media(self, ui: Task):
        """
        The algorithm for synchronizing profile photo and video avatars to 
        the recipient's essence.
        """
        sender = self.client(self.database.get_session_by_status(1))
        recepient = self.client(self.database.get_session_by_status(0))

        if not (sender.is_connected() and recepient.is_connected()):
            await sender.connect()
            await recepient.connect()

        image_extension = ".jpeg"
        video_extension = ".mp4"
        photo: Photo
        try:
            i = 0
            photos = await sender.get_profile_photos("me")
            ui.progress_counters.visible = True
            ui.total.value = photos.total
            for photo in reversed(photos):
                i += 1
                ui.progress.value = i / photos.total
                ui.value.value = i
                ui.update()
                await asyncio.sleep(3)
                blob = await sender.download_media(photo, bytes)
                name = "Syncogram_" + datetime.strftime(
                    photo.date, "%Y_%m_%d_%H_%M_%S"
                )
                if not photo.video_sizes:
                    file = await recepient.upload_file(
                        blob,
                        file_name=name + image_extension
                    )
                    await recepient(UploadProfilePhotoRequest(file=file))
                    continue
                file = await recepient.upload_file(
                    blob,
                    file_name=name + video_extension
                )
                await recepient(UploadProfilePhotoRequest(video=file))
        except Exception as e:
            return ui.unsuccess(e)
        finally:
            sender.disconnect()
            recepient.disconnect()

        ui.success()

    async def sync_public_channels(self, ui: Task):
        pass