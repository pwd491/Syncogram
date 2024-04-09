from os import getenv
from asyncio import sleep

from dotenv import load_dotenv
import flet as ft


from .client import UserClient
from ..database import SQLite
from .task import CustomTask

load_dotenv()

class Manager:
    def __init__(self, mainwindow = None) -> None:
        self.database = SQLite()
        self.mainwindow = mainwindow
        self.session: str = getenv("AUTH_TOKEN", "AUTH_TOKEN")

        self.sender = UserClient()
        self.recipient = UserClient()

        self.options = {
            "is_sync_fav": {
                "title": "Sync my favorite messages between accounts.",
                "function": self.sync_favorite_messages,
                "status": bool()
            },
            "is_sync_pin_fav": {
                "title": "Sync sequence of pinned messages in favorite messages.",
                "function": self.sync_sequence_of_pinned_messages,
                "status": bool()
            },
            "is_sync_profile_name": {
                "title": "Sync profile first name and second name.",
                "function": self.sync_profile_first_name_and_second_name,
                "status": bool()
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
        print("Синхронизация личных сооьщений")
        await sleep(3)
        ui_task_object.border = ft.Border = ft.border.all(0.5, ft.colors.GREEN)
        await ui_task_object.update_async()

        # if not self.sender.is_connected():
            # await self.sender.connect()

        # data = await self.sender.get_messages("me")

        # self.sender.disconnect()

    async def sync_sequence_of_pinned_messages(self, ui_task_object: CustomTask):
        print("Синхронизация закрепов")
        await sleep(3)
        ui_task_object.border = ft.Border = ft.border.all(0.5, ft.colors.GREEN)
        await ui_task_object.update_async()


    async def sync_profile_first_name_and_second_name(self, ui_task_object: CustomTask):
        # if not self.sender.is_connected():
        #     await self.sender.connect()

        # data = await self.sender.get_messages("me")

        # self.sender.disconnect()
        print("Синхронизация имени и фамилии")
        await sleep(3)
        ui_task_object.border = ft.Border = ft.border.all(0.5, ft.colors.GREEN)
        await ui_task_object.update_async()

    async def start_all_tasks(self, e):
        for option in self.options.items():
            if option[1].get("status"):
                func = option[1].get("function")
                obj = option[1].get("ui_task_object")

                await func(obj)