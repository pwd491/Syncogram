"""The main file to run application."""
import flet as ft

from sourcefiles import UserBar
from sourcefiles import MainWindow
from sourcefiles import WelcomeScreenAnimation
from sourcefiles import UpdateApplicationAlert
from sourcefiles.utils import config
from sourcefiles.utils import get_locale

cfg = config()
_ = get_locale(__file__)

async def application(page: ft.Page) -> None:
    """Entry point of application"""
    page.title = cfg["APP"]["NAME"]
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
    UpdateApplicationAlert(page, _)

if __name__ == "__main__":
    ft.app(target=application, assets_dir="assets")
