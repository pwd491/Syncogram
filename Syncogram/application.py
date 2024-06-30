import flet as ft

from sourcefiles import WelcomeScreenAnimation
from sourcefiles import UpdateApplicationAlert
from sourcefiles import TheScreensController
from sourcefiles import get_locale
from sourcefiles import logging

logger = logging()

@logger.catch()
def main(page: ft.Page) -> None:
    """The entry point to start application."""
    page.title = "Syncogram"
    page.window.width = page.window.min_width = 960
    page.window.height = page.window.min_height = 680
    page.theme_mode = ft.ThemeMode.DARK
    page.window.center()
    _: str = get_locale(__file__, page)

    WelcomeScreenAnimation(page, _)
    TheScreensController(page, _)
    UpdateApplicationAlert(page, _)

if __name__ == '__main__':
    ft.app(main, assets_dir="assets")
