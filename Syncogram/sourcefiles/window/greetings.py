from asyncio import sleep
from typing import Any

import flet as ft

from .stickers import DUCK_STICKER_IT
from ..config import APP_NAME

class WelcomeScreenAnimation(ft.Container):
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page: ft.Page = page

        self.title = ft.Text()
        self.title.value = APP_NAME.upper()
        self.title.size = 72
        self.title.color = ft.colors.WHITE
        self.title.weight = ft.FontWeight.W_600

        self.subtitle = ft.Text()
        self.subtitle.value = _("Fast, secure and reliable synchronization of information").upper()
        self.subtitle.size = 12.3
        self.subtitle.opacity = 0
        self.subtitle.animate_opacity = ft.Animation(1000, ft.AnimationCurve.EASE_IN)

        self.logo = ft.Column([self.title, self.subtitle])
        self.logo.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.animate_duration = 1000
        self.image = ft.Image()
        self.image.src_base64 = DUCK_STICKER_IT
        self.image.scale = ft.transform.Scale(1)
        self.image.animate_scale = ft.Animation(
            self.animate_duration,
            ft.AnimationCurve.EASE_IN_TO_LINEAR
        )

        self.greetings_wrapper = ft.Column([self.logo])
        self.greetings_wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.greetings_wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.wrapper = ft.Row([self.greetings_wrapper])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.expand = True

        self.content = self.wrapper
        self.expand = True

    async def __call__(self):
        self.page.add(self)
        await sleep(0.5)
        self.subtitle.opacity = 1
        self.subtitle.update()
        await sleep(2)
        self.page.remove(self)
