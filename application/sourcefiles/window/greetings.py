from asyncio import sleep
import flet as ft

from .stickers import DUCK_STICKER_IT

class WelcomeScreenAnimation(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page

        self.image = ft.Image()
        self.image.src_base64 = DUCK_STICKER_IT
        self.image.scale = ft.transform.Scale(1)
        self.image.animate_scale = ft.Animation(600, ft.AnimationCurve.EASE)

        self.greetings_wrapper = ft.Column([self.image])
        self.greetings_wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.greetings_wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.wrapper = ft.Row([self.greetings_wrapper])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.expand = True


        self.content = self.wrapper
        self.expand = True

    async def did_mount_async(self):
        await sleep(2.25)
        self.image.scale = 0
        await self.image.update_async()
        await sleep(1.25)
