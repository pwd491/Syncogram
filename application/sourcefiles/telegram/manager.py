from os import getenv
from asyncio import sleep

from telethon.tl.functions.account import UpdateProfileRequest
from dotenv import load_dotenv
import flet as ft
from telethon.tl.types import InputPeerUser, User


from .client import UserClient
from ..database import SQLite
from .task import CustomTask

load_dotenv()

class Manager:
    def __init__(self, mainwindow = None) -> None:
        self.database = SQLite()
        self.mainwindow = mainwindow
        self.session: str = getenv("AUTH_TOKEN", "AUTH_TOKEN")
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
                "title": "Synchronize the first and last name of the profile.",
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
        await self.mainwindow.update_async()


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


    async def sync_sequence_of_pinned_messages(self, ui_task_object: CustomTask):
        print("Синхронизация закрепов")
        await sleep(3)
        ui_task_object.border = ft.Border = ft.border.all(0.5, ft.colors.GREEN)
        await ui_task_object.update_async()


    async def sync_profile_first_name_and_second_name(self, ui_task_object: CustomTask):
        ui_task_object.progress.value = None
        await ui_task_object.progress.update_async()

        self.sender = self.client(*self.database.get_user_by_status(1))
        self.recepient = self.client(*self.database.get_user_by_status(0))
        if not (self.sender.is_connected() and self.recepient.is_connected()):
            await self.sender.connect()
            await self.recepient.connect()

        try:
            data: User | InputPeerUser = await self.sender.get_me()
            first_name = data.first_name
            last_name = data.last_name
            await self.recepient(UpdateProfileRequest(first_name, last_name))
        except Exception as e:
            ui_task_object.progress.value = 0
            ui_task_object.header.controls.pop(-1)
            ui_task_object.header.controls.append(ft.Icon(ft.icons.ERROR, color=ft.colors.RED, tooltip=str(e)))
            ui_task_object.border = ft.border.all(0.5, ft.colors.RED)
            return await ui_task_object.update_async()


        self.sender.disconnect()
        self.recepient.disconnect()
        ui_task_object.progress.value = 1
        ui_task_object.header.controls.pop(-1)
        ui_task_object.header.controls.append(ft.Icon(ft.icons.TASK_ALT, color=ft.colors.GREEN))
        ui_task_object.border = ft.border.all(0.5, ft.colors.GREEN)
        await ui_task_object.update_async()

    async def start_all_tasks(self, e):
        for option in self.options.items():
            if option[1].get("status"):
                func = option[1].get("function")
                obj = option[1].get("ui_task_object")

                await func(obj)