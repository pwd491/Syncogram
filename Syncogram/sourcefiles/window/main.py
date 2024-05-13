from asyncio import sleep
from asyncio import gather
from functools import partial

import flet as ft

from ..database import SQLite
from ..telegram import Manager


class ButtonStartTasks(ft.Container):
    def __init__(self, manager, _) -> None:
        super().__init__()
        self.manager = manager
        self.state = False

        self.button_start_wrapper_icon = ft.Icon()
        self.button_start_wrapper_icon.color = ft.colors.WHITE
        self.button_start_wrapper_icon.name = ft.icons.SYNC
        self.button_start_wrapper_icon.rotate = ft.transform.Rotate(0, ft.alignment.center)
        self.button_start_wrapper_icon.animate_rotation = ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT)
        self.button_start_wrapper_text = ft.Text()
        self.button_start_wrapper_text.value = _("START")
        self.button_start_wrapper_text.weight = ft.FontWeight.W_600
        self.button_start_wrapper = ft.Row([])
        self.button_start_wrapper.controls = [
            self.button_start_wrapper_icon,
            self.button_start_wrapper_text,
        ]
        self.border_radius = ft.BorderRadius(50,50,50,50)
        self.padding = ft.Padding(20, 10, 20, 10)
        self.content = self.button_start_wrapper
        self.bgcolor = ft.colors.BLUE
        self.on_click = partial(self.click, _=_)
        self.animate_rotation = ft.Animation(500, ft.AnimationCurve.SLOW_MIDDLE)
    
    async def click(self, e: ft.ContainerTapEvent, _) -> None:
        self.state = True
        self.button_start_wrapper_text.visible = False
        self.update()
        await gather(self.infinity_rotate(), self.manager.start_all_tasks(self, _))
        self.button_start_wrapper_text.visible = True
        self.update()
        

    async def infinity_rotate(self):
        while self.state:
            await sleep(0.1)
            self.button_start_wrapper_icon.rotate.angle += 1
            self.button_start_wrapper_icon.update()


    def did_mount(self):
        return self


class MainWindow(ft.Container):
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page = page
        self.database = SQLite()
        self.database.check_update()
        self.manager = Manager(self.page, _, self)
        self.button_start = ButtonStartTasks(self.manager, _)

        self.sticker = ft.Image()
        self.sticker.src = "stickers/sticker2.gif"
        self.sticker.width = 200
        self.sticker_text = ft.Text( _("To get started, log in to at least 2 accounts") )


        self.welcome = ft.Row([
            ft.Column([
                self.sticker,
                self.sticker_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ])
        self.welcome.alignment = ft.MainAxisAlignment.CENTER



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