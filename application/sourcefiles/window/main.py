import asyncio
from cmath import pi
from functools import partial
import flet as ft

from .stickers import DUCK_STICKER_HI
from ..database import SQLite
from ..telegram import Manager


class MainWindow(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.database = SQLite()
        self.manager = Manager(self)

        self.sticker = ft.Image()
        self.sticker.src_base64 = DUCK_STICKER_HI
        self.sticker.width = 200
        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")


        self.welcome = ft.Row([ft.Column([self.sticker, self.sticker_text])])
        self.welcome.alignment = ft.MainAxisAlignment.CENTER


        # self.button_start = ft.IconButton()
        self.button_start_wrapper_icon = ft.Icon()
        self.button_start_wrapper_icon.color = ft.colors.WHITE
        self.button_start_wrapper_icon.name = ft.icons.SYNC
        self.button_start_wrapper_icon.rotate = ft.transform.Rotate(0, ft.alignment.center)
        self.button_start_wrapper_text = ft.Text()
        self.button_start_wrapper_text.value = "START"
        self.button_start_wrapper_text.weight = ft.FontWeight.W_600
        self.button_start_wrapper = ft.Row([])
        self.button_start_wrapper.controls = [
            self.button_start_wrapper_icon,
            self.button_start_wrapper_text,
        ]
        self.button_start = ft.Container()
        self.button_start.border_radius = ft.BorderRadius(50,50,50,50)
        self.button_start.padding = ft.Padding(20, 10, 30, 10)
        self.button_start.content = self.button_start_wrapper
        self.button_start.bgcolor = ft.colors.BLUE
        self.button_start.on_click = partial(
            self.manager.start_all_tasks,
            btn=self.button_start
        )
        self.button_start.on_hover = self.hover_animate
        self.button_start.animate_rotation = ft.Animation(500, ft.AnimationCurve.SLOW_MIDDLE)

        self.wrapper_side_column = ft.Column([])
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

    async def hover_animate(self, e):
        while bool(e.data):
            # await asyncio.sleep(3)
            print(bool(e.data))
            self.button_start_wrapper_icon.rotate.angle += 0.1
            self.button_start_wrapper_icon.update()
            

    
    async def callback_update(self) -> None:
        users = self.database.get_users()
        self.wrapper.controls.clear()
        self.wrapper_side_column.controls.clear()
        if len(users) < 2:
            self.wrapper.controls.append(self.welcome)
            self.wrapper.alignment = ft.MainAxisAlignment.CENTER
            return self.update()

        self.wrapper.controls.append(self.wrapper_side)
        self.wrapper.controls.append(self.wrapper_footer)
        await self.manager.build()

        self.update()

    def did_mount(self) -> None:
        self.page.run_task(self.callback_update)