import asyncio
import time

import flet as ft


class WelcomeScreenAnimation(ft.Container):
    """Greeting screen animations."""
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page: ft.Page = page

        self.title = ft.Text()
        self.title.value = "Syncogram".upper()
        self.title.size = 72
        self.title.color = ft.colors.WHITE
        self.title.weight = ft.FontWeight.W_600

        self.subtitle = ft.Text()
        self.subtitle.value = _(
            "Fast, secure and reliable synchronization of information"
        ).upper()
        self.subtitle.size = 12.3
        self.subtitle.opacity = 0
        self.subtitle.animate_opacity = ft.Animation(1000, ft.AnimationCurve.EASE_IN)

        self.logo = ft.Column([self.title, self.subtitle])
        self.logo.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.greetings_wrapper = ft.Column([self.logo])
        self.greetings_wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.greetings_wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.wrapper = ft.Row([self.greetings_wrapper])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.expand = True

        self.content = self.wrapper
        self.expand = True
        self.callback()

    async def display(self):
        self.page.add(self)
        await asyncio.sleep(0.5)
        self.subtitle.opacity = 1
        self.subtitle.update()
        await asyncio.sleep(2)
        self.page.remove(self)

    def callback(self):
        self.page.run_task(self.display)
        time.sleep(2)
