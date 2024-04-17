import gettext
import flet as ft

from sourcefiles import UserBar
from sourcefiles import MainWindow
from sourcefiles import WelcomeScreenAnimation
from sourcefiles.utils import newest_version
from sourcefiles.config import (
    APP_VERSION,
    APP_NAME
)

translations = gettext.translation('base', './locales', fallback=True)
_ = translations.gettext

async def application(page: ft.Page) -> None:
    page.title = APP_NAME
    page.window_width = page.window_min_width = 960
    page.window_height = page.window_min_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window_center()

    mainwindow = MainWindow(page, _)
    userbar = UserBar(page, mainwindow.callback_update, _)
    await WelcomeScreenAnimation(page, _)()

    page.add(
        ft.Row(
            [
                userbar,
                mainwindow,
            ],
            expand=True,
        )
    )
    newest_version(page, APP_VERSION, _)

if __name__ == "__main__":
    ft.app(target=application, assets_dir="assets")
