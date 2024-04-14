import flet as ft

from sourcefiles import UserBar
from sourcefiles import MainWindow
from sourcefiles import WelcomeScreenAnimation
from sourcefiles.utils import check_newest_version
from sourcefiles.config import (
    APP_VERSION,
    APP_NAME
)

async def application(page: ft.Page) -> None:
    page.title = APP_NAME
    page.window_width = page.window_min_width = 960
    page.window_height = page.window_min_height = 680
    await page.window_center_async()
    page.theme_mode = ft.ThemeMode.DARK

    mainwindow = MainWindow(page)
    userbar = UserBar(page, mainwindow.updateme)
    greetings = WelcomeScreenAnimation(page)


    await page.add_async(greetings)
    await page.remove_async(greetings)


    await page.add_async(
        ft.Row(
            [
                userbar,
                mainwindow,
            ],
            expand=True,
        )
    )

    await check_newest_version(page, APP_VERSION)
    await page.update_async()


if __name__ == "__main__":
    ft.app(target=application, assets_dir="assets")
