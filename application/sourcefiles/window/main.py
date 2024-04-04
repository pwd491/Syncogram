import flet as ft

from .task import CustomTask
from ..database import SQLite

class CustomTaskWrapper(ft.Container):
    def __init__(self):
        super().__init__()

        self.wrapper = ft.Row()
        self.content = self.wrapper
        self.width = 450
        self.height = 100
        self.bgcolor = "yellow"

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

        
        self.button_start = ft.FilledButton()
        self.button_start.text = "Start"

        # self.wrapper

        self.wrapper_side = ft.Container()
        self.wrapper_side.content = ft.Column()
        self.wrapper_side.bgcolor = "red"
        # self.wrapper_side.expand = True
        self.wrapper_side.content.alignment = ft.MainAxisAlignment.CENTER

        self.wrapper_side.content.controls.append(CustomTaskWrapper())

        self.wrapper_footer = ft.Container()
        self.wrapper_footer.content = ft.Row()
        self.wrapper_footer.content.alignment = ft.MainAxisAlignment.END
        self.wrapper_footer.content.controls.append(self.button_start)
        # self.wrapper_footer.bgcolor = "yellow"
        self.wrapper_footer.height = 50


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
        if len(users) < 2:
            self.wrapper.controls.append(self.welcome)
            return await self.update_async()
        
        self.wrapper.controls.append(self.wrapper_side)
        self.wrapper.controls.append(self.wrapper_footer)

        await self.update_async()