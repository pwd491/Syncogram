import flet as ft

from ..database import SQLite
from ..telegram import Manager


class MainWindow(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.database = SQLite()
        self.manager = Manager(self)

        self.sticker = ft.Image()
        self.sticker.src = "stickers/sticker2.gif"
        self.sticker.width = 200
        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")


        self.welcome = ft.Row([ft.Column([self.sticker, self.sticker_text])])
        self.welcome.alignment = ft.MainAxisAlignment.CENTER


        self.button_start = ft.ElevatedButton()
        self.button_start.bgcolor = ft.colors.BLUE_700
        self.button_start.color = ft.colors.WHITE
        self.button_start.text = "START"
        self.button_start.icon = ft.icons.SYNC
        self.button_start.height = 40
        self.button_start.on_click = self.manager.sync_favorite_messages


        self.wrapper_side_column = ft.Column([
            # CustomTask(),
            # CustomTask(),
            # CustomTask(),
        ])
        self.wrapper_side_column.expand = True
        self.wrapper_side_column.alignment = ft.MainAxisAlignment.START
        self.wrapper_side_column.scroll = ft.ScrollMode.AUTO
      

        self.wrapper_side = ft.Container()
        self.wrapper_side.content = ft.Row([self.wrapper_side_column])
        self.wrapper_side.expand = True


        self.wrapper_footer = ft.Container()
        self.wrapper_footer.content = ft.Row([self.button_start])
        self.wrapper_footer.content.alignment = ft.MainAxisAlignment.END
        self.wrapper_footer.height = 50
        self.wrapper_footer.border_radius = ft.BorderRadius(10,10,10,10)
        self.wrapper_footer.bgcolor = ft.colors.BLACK12


        self.wrapper = ft.Column()
        self.content = self.wrapper
        self.expand = True
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.padding = 20

    async def did_mount_async(self) -> None:
        await self.manager.build()
        await self.updateme()

    async def updateme(self) -> None:
        users = self.database.get_users()
        self.wrapper.controls.clear()
        if len(users) < 2:
            self.wrapper.controls.append(self.welcome)
            self.wrapper.alignment = ft.MainAxisAlignment.CENTER
            return await self.update_async()

        self.wrapper.controls.append(self.wrapper_side)
        self.wrapper.controls.append(self.wrapper_footer)

        await self.update_async()
