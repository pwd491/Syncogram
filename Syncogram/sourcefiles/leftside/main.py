import flet as ft

from .accounts import Accounts
from ..database import SQLite
from ..components import SettingsButton
from ..components import AboutApplication
from ..components import FeedBack
from ..utils import logging

logger = logging()

class Userbar(ft.Container):
    """Userbar container side."""
    @logger.catch()
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page = page
        self.database = SQLite()
        self._: str = _

        self.feedback = ft.Row(
            [FeedBack(self._)], alignment=ft.MainAxisAlignment.CENTER
        )

        self.about = ft.Row(
            [AboutApplication(self._)], alignment=ft.MainAxisAlignment.CENTER
        )

        self.settings = ft.Row(
            [SettingsButton(self.page, self._)],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.accounts = Accounts(self.page, self._)
        logger.info("Accounts side was builded.")
        
        self.bottom = ft.Column([
            self.feedback,
            self.about,
            ft.Divider(),
            self.settings
        ])
        self.top = ft.Column([self.accounts])

        self.content = ft.Column([self.top, self.bottom])
        self.content.alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.width = 250
        self.padding = 20
        logger.info("Userbar was builded.")

    def callback(self) -> None:
        """Regenerate accounts side."""
        self.accounts.callback()
        self.accounts.update()
