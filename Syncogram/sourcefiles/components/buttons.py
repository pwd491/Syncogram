import asyncio
from math import pi

import flet as ft

from .settings import Settings
from .warnings import CancelAllTasksDialog

class SettingsButton(ft.ElevatedButton):
    """Settings button open dialog."""
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page: ft.Page = page
        self._ = _
        self.settings = Settings(self.page, self._)

        self.text = _("Settings")
        self.icon = ft.icons.SETTINGS
        self.expand = True
        self.height = 45
        self.on_click = self.__open

    async def __open(self, e):
        self.page.dialog = self.settings
        self.page.update()
        self.settings.open = True
        self.settings.update()


class StartAllTasksButton(ft.Container):
    """Class of Button to executes all set tasks in application."""

    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page = page
        self._ = _
        self.state = False
        self.event = asyncio.Event()
        # self.manager = manager
        self.cancel = CancelAllTasksDialog(self.page, self.event, self._)
        self.width = 140

        self.icon = ft.Icon()
        self.icon.color = ft.colors.WHITE
        self.icon.name = ft.icons.SYNC
        self.icon.rotate = ft.transform.Rotate(0, ft.alignment.center)
        self.icon.animate_rotation = ft.animation.Animation(
            300, ft.AnimationCurve.BOUNCE_OUT
        )
        self.label_start = self._("Start").upper()
        self.label_cancel = self._("Stop").upper()

        self.text = ft.Text()
        self.text.value = self.label_start
        self.text.weight = ft.FontWeight.W_500
        self.text.offset = ft.Offset(0, 0)
        self.text.animate_offset = ft.animation.Animation(
            300, ft.AnimationCurve.FAST_OUT_SLOWIN
        )

        self.button_start_wrapper = ft.Row([])
        self.button_start_wrapper.controls = [
            self.icon,
            self.text,
        ]

        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            # colors=[
            #     "0xff1f005c",
            #     "0xff5b0060",
            #     "0xff870160",
            #     "0xffac255e",
            #     "0xffca485c",
            #     "0xffe16b5c",
            #     "0xfff39060",
            #     "0xffffb56b",
            # ],
            colors=[
                "0xff2c3e52",
                "0xfffd746a",
            ],
            tile_mode=ft.GradientTileMode.MIRROR,
            # rotation=pi / 3
        )

        self.border_radius = ft.BorderRadius(50, 50, 50, 50)
        self.padding = ft.Padding(25, 10, 25, 10)
        self.content = self.button_start_wrapper
        self.bgcolor = self.gradient
        self.on_click = self.__click
        self.on_hover = self.__hover

    async def __hover(self, e):
        if e.data == "true":
            if not self.state:
                self.opacity = 0.9
                self.icon.rotate.angle -= 3
                self.update()
        else:
            self.opacity = 1
            self.update()

    async def __click(self, e):
        if not self.state:
            self.state = True
            self.text.offset.x += 5.0
            self.text.update()
            await asyncio.sleep(0.3)
            self.text.value = self.label_cancel
            self.text.offset.x -= 5.0
            self.text.update()
            await self.infinity_rotate()
        else:
            self.page.dialog = self.cancel
            self.page.dialog.open = True
            self.page.update()
            await self.cancel()
            self.state = False
            self.text.offset.x += 5.0
            self.text.update()
            await asyncio.sleep(0.3)
            self.text.value = self.label_start
            self.text.offset.x -= 5.0
            self.text.update()
            self.update()

    async def infinity_rotate(self):
        """Animation of the progress icon."""
        while self.state:
            await asyncio.sleep(0.1)
            self.icon.rotate.angle -= 1
            self.icon.update()
