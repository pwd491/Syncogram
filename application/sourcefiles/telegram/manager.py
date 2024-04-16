from asyncio import sleep

import flet as ft
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPeerUser, User, UserFull

from .client import UserClient
from .task import CustomTask
from ..database import SQLite

class Manager:
    def __init__(self, mainwindow = None) -> None:
        self.database = SQLite()
        self.mainwindow = mainwindow
        self.client = UserClient
    
        self.options = {
            "is_sync_fav": {
                "title": "Sync my favorite messages between accounts.",
                "function": self.sync_favorite_messages,
                "status": bool(),
                "ui_task_object": CustomTask
            },
            "is_sync_pin_fav": {
                "title": "Synchronize the sequence of pinned messages in your favorite messages.",
                "function": self.sync_sequence_of_pinned_messages,
                "status": bool(),
                "ui_task_object": CustomTask
            },
            "is_sync_profile_name": {
                "title": "Synchronize the first name, last name and biography of the profile.",
                "function": self.sync_profile_first_name_and_second_name,
                "status": bool(),
                "ui_task_object": CustomTask
            }
        }

    async def build(self):
        list_of_options = self.database.get_options()[1:]
        
        for n, option in enumerate(self.options.items()):
            option[1].update({"status": bool(list_of_options[n])})

        for option in self.options.items():
            if option[1].get("status"):
                title = option[1].get("title")
                task = CustomTask(title)
                option[1].update(
                    {
                        "ui_task_object": task
                    }
                )
                self.mainwindow.wrapper_side_column.controls.append(task)
        self.mainwindow.update()


    async def sync_favorite_messages(self, ui_task_object: CustomTask):
        """
        Важно учитывать:
        a. Последовательность отвеченных сообщений
        b. Контекст сообщения, для навигации используют хештег
        c. Статус о закреплении сообщения в диалоге
        
        Важно итерировать диалог, таким образом получится достичь максимума
        информации для каждого сообщения. Стоит коолекционировать данные, для
        следующих функций, где мы могли бы переиспользовать эти данные.
        """
        pass

    async def sync_sequence_of_pinned_messages(self, ui_task_object: CustomTask):
        print("Синхронизация закрепов")
        await sleep(3)
        ui_task_object.progress.value = 1
        ui_task_object.header.controls.pop(-1)
        ui_task_object.header.controls.append(ft.Icon(ft.icons.TASK_ALT, color=ft.colors.GREEN))
        ui_task_object.border = ft.Border = ft.border.all(0.5, ft.colors.GREEN)
        ui_task_object.update()


    async def sync_profile_first_name_and_second_name(self, ui_task_object: CustomTask):
        ui_task_object.progress.value = None
        ui_task_object.progress.update()

        self.sender = self.client(*self.database.get_user_by_status(1))
        self.recepient = self.client(*self.database.get_user_by_status(0))

        if not (self.sender.is_connected() and self.recepient.is_connected()):
            await self.sender.connect()
            await self.recepient.connect()

        try:
            user: UserFull = await self.sender(GetFullUserRequest("me"))
            first_name = user.users[0].first_name
            last_name = user.users[0].last_name
            bio = user.full_user.about 
            await self.recepient(UpdateProfileRequest(first_name, last_name, bio))
        except Exception as e:
            return ui_task_object.unsuccess(e)

        self.sender.disconnect()
        self.recepient.disconnect()
        ui_task_object.success()

    async def start_all_tasks(self, e, btn: ft.IconButton):
        # for option in self.options.items():
        #     if option[1].get("status"):
        #         func = option[1].get("function")
        #         obj = option[1].get("ui_task_object")
                # await func(obj)
                # btn.text = ""
                btn.update()