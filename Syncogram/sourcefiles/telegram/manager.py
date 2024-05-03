import asyncio

import flet as ft
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.patched import MessageService
from telethon.tl.types import UserFull, PeerUser, Message

from .client import UserClient
from .task import CustomTask
from ..database import SQLite
from ..userbar.settings import SettingsDialog


class Manager:
    def __init__(self, page: ft.Page, _, mainwindow=None) -> None:
        self.page: ft.Page = page
        self.database = SQLite()
        self.mainwindow = mainwindow
        self.client = UserClient

        self.options = {
            "is_sync_fav": {
                "title": _("Sync my favorite messages between accounts."),
                "function": self.sync_favorite_messages,
                "status": bool(),
                "ui_task_object": CustomTask,
            },
            "is_sync_profile_name": {
                "title": _(
                    "Synchronize the first name, last name and biography of the profile."
                ),
                "function": self.sync_profile_first_name_and_second_name,
                "status": bool(),
                "ui_task_object": CustomTask,
            },
        }

    async def build(self):

        list_of_options = self.database.get_options()
        if list_of_options is None:
            return
        list_of_options = list_of_options[1:]

        for n, option in enumerate(self.options.items()):
            option[1].update({"status": bool(list_of_options[n])})

        for option in self.options.items():
            if option[1].get("status"):
                title = option[1].get("title")
                task = CustomTask(title)
                option[1].update({"ui_task_object": task})
                self.mainwindow.wrapper_side_column.controls.append(task)
        self.mainwindow.update()

    async def sync_favorite_messages(self, ui_task_object: CustomTask):
        # ui_task_object.progress.value = None
        # ui_task_object.progress.update()

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
            ui_task_object.progress_counters.visible = True
            i = 0
            async for message in source_messages:
                i += 1
                ui_task_object.total.value = source_messages.total
                ui_task_object.progress.value = i / source_messages.total
                ui_task_object.value.value = i
                ui_task_object.update()
                # await asyncio.sleep(0.00001)
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
            return ui_task_object.unsuccess(e)
        finally:
            del msg_ids
            sender.disconnect()
            recepient.disconnect()

        ui_task_object.success()

    async def sync_profile_first_name_and_second_name(self, ui_task_object: CustomTask):
        """
        Connecting accounts, getting profile data and sets.
        """
        ui_task_object.progress.value = None
        ui_task_object.progress.update()

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
            return ui_task_object.unsuccess(e)

        sender.disconnect()
        recepient.disconnect()
        ui_task_object.success()

    async def start_all_tasks(self, btn, _):
        if not 1 in self.database.get_options()[1:]:
            settings = SettingsDialog(self.mainwindow.callback_update, _)
            self.page.dialog = settings
            settings.open = True
            btn.state = False
            return self.page.update()

        for option in self.options.items():
            if option[1].get("status"):
                func = option[1].get("function")
                obj = option[1].get("ui_task_object")
                await func(obj)
        btn.state = False
        btn.update()
