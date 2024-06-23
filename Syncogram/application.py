import flet as ft

from sourcefiles import WelcomeScreenAnimation
from sourcefiles import UpdateApplicationAlert
from sourcefiles import TheScreensController
from sourcefiles import get_locale
from sourcefiles import logging

logger = logging()
_: str = get_locale(__file__)

@logger.catch()
def main(page: ft.Page) -> None:
    """The entry point to start application."""
    page.title = "Syncogram"
    page.window_width = page.window_min_width = 960
    page.window_height = page.window_min_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window_center()

    WelcomeScreenAnimation(page, _)
    TheScreensController(page, _)
    UpdateApplicationAlert(page, _)

if __name__ == '__main__':
    ft.app(main, assets_dir="assets")
