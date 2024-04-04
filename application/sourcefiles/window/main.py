import flet as ft

from .task import CustomTask
from ..database import SQLite

class MainWindow(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.database = SQLite()

        self.sticker = ft.Image()
        self.sticker.src = "stickers/sticker2.gif"
        self.sticker.width = 200

        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")
        self.welcome = ft.Column([self.sticker, self.sticker_text])
        self.welcome.alignment = ft.MainAxisAlignment.CENTER
        self.welcome.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.wrapper = ft.Column()

        self.content = self.wrapper
        self.expand = True
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.padding = 20

    async def did_mount_async(self):
        await self._update()

    async def _update(self):
        users = self.database.get_users()
        if len(users) >= 2:
            self.wrapper.controls.append(CustomTask())
            self.wrapper.controls.append(CustomTask())
            self.wrapper.controls.append(CustomTask())
            self.wrapper.controls.append(CustomTask())
            self.wrapper.controls.append(CustomTask())

        else:
            self.wrapper.controls.append(self.welcome)
            self.wrapper.alignment = ft.MainAxisAlignment.CENTER
            self.wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        await self.update_async()