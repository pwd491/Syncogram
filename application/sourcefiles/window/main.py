from tkinter.ttk import Progressbar
from turtle import width
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

        
        self.button_start = ft.TextButton()
        self.button_start.text = "Start syncing"
        self.button_start.icon = ft.icons.SYNC
        self.button_start.height = 40


        class Task(ft.Container):
            def __init__(self):
                super().__init__()

                self.wrapper = ft.Column([
                    ft.Text("Sync my favorite messages."),
                    ft.Divider(color="white"),
                    ft.ProgressBar(width=500, value=0),
                ])

                self.content = ft.Row([self.wrapper])
                self.height = 100
                self.bgcolor = ft.colors.BLACK38
                self.border_radius = ft.BorderRadius(10,10,10,10)
                self.border = ft.border.all(0.5, ft.colors.ORANGE)
                self.padding = 20


        self.wrapper_side_column = ft.Column([
            Task(),
            Task(),
            Task(),
            Task(),
            Task(),
            Task(),
            Task(),
            Task(),
            Task(),
        ])
        self.wrapper_side_column.expand = True
        self.wrapper_side_column.alignment = ft.MainAxisAlignment.START
        self.wrapper_side_column.scroll = ft.ScrollMode.AUTO
      
        self.wrapper_side = ft.Container()
        self.wrapper_side.content = ft.Row([self.wrapper_side_column])
        # self.wrapper_side.bgcolor = "red"
        self.wrapper_side.expand = True


        self.wrapper_footer = ft.Container()
        self.wrapper_footer.content = ft.Row([self.button_start])
        self.wrapper_footer.content.alignment = ft.MainAxisAlignment.END
        # self.wrapper_footer.bgcolor = "yellow"
        self.wrapper_footer.height = 50
        self.wrapper_footer.border_radius = ft.BorderRadius(10,10,10,10)
        self.wrapper_footer.bgcolor = ft.colors.BLACK12


        self.wrapper = ft.Column(
            [
                self.wrapper_side,
                self.wrapper_footer
            ]
        )

        self.content = self.wrapper
        self.content.visible = False
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
        
        self.content.visible = True

        await self.update_async()