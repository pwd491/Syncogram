"""The main file to run application."""
import os
import gettext
import flet as ft

from locale import getlocale

from sourcefiles import UserBar
from sourcefiles import MainWindow
from sourcefiles import WelcomeScreenAnimation
from sourcefiles.utils import config
from sourcefiles.utils import newest_version


cfg = config()

path_to_locales = os.path.abspath(os.path.join(os.path.dirname(__file__), "locales"))

DOMAIN = "base"

ru = gettext.translation(DOMAIN, path_to_locales, ["ru"], fallback=True)
en = gettext.translation(DOMAIN, path_to_locales, ["en"], fallback=True)

if getlocale()[0] in ["Russian_Russia","ru_RU"]:
    ru.install()
    _ = ru.gettext
else:
    en.install()
    _ = en.gettext

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
    newest_version(page, _)

if __name__ == "__main__":
    ft.app(target=application, assets_dir="assets")
