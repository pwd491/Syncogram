from os import getenv

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
            }
        }


    async def build(self):
        list_of_options = self.database.get_options()[1:]
        
        for n, option in enumerate(self.options.items()):
            option[1].update({"status": bool(list_of_options[n])})

        for option in self.options.items():
            if option[1].get("status"):
                title: str = option[1].get("title")
                task = CustomTask(title)
                option[1].update(
                    {
                        "ui_task_object": task
                    }
                )
                self.mainwindow.wrapper_side_column.controls.append(task)
        await self.mainwindow.update_async()


    async def sync_favorite_messages(self, e):
        """
        Важно учитывать:
        a. Последовательность отвеченных сообщений
        b. Контекст сообщения, для навигации используют хештег
        c. Статус о закреплении сообщения в диалоге
        
        Важно итерировать диалог, таким образом получится достичь максимума
        информации для каждого сообщения. Стоит коолекционировать данные, для
        следующих функций, где мы могли бы переиспользовать эти данные.
        """
        await self.build()


        # task = CustomTask("Hello world")
        # self.mainwindow.wrapper_side_column.controls.append(task)
        # await self.mainwindow.update_async()


        test_btn = ft.TextButton("asd", on_click=self.btn)

        self.mainwindow.wrapper_side_column.controls.append(test_btn)

        await self.mainwindow.update_async()
        # if not self.sender.is_connected():
            # await self.sender.connect()

        # data = await self.sender.get_messages("me")

        # self.sender.disconnect()

    async def btn(self, e):
        x = self.options.get("is_sync_fav")
        obj: CustomTask = x.get("ui_task_object")
        obj.border = ft.border.all(0.5, ft.colors.GREEN)
        await obj.update_async()

    async def sync_sequence_of_pinned_messages(self):
        pass