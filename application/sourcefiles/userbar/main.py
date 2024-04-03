import flet as ft

from .settings import SettingsDialog
from .generate import UIGenerateAccounts
from ..database import SQLite


class UserBar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.database = SQLite()
        self.page: ft.Page = page
        self.generate_accounts = UIGenerateAccounts(self.page)

        # Buttons
        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        self.settings_btn.height = 45
        self.settings_btn.on_click = self.settings

        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"

        # Containers
        self.wrapper_accounts_side: UIGenerateAccounts = self.generate_accounts

        self.wrapper_settings = ft.Container(ft.Row([self.settings_btn]))
        self.wrapper_settings.width = 200
        self.wrapper_settings.height = 50

        # Main block like canvas to display controls
        self.content = ft.Column(
            [
                self.wrapper_accounts_side,
                self.wrapper_settings,
            ]
        )
        self.width = 250
        self.padding = 20
        self.content.expand = True
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    async def settings(self, e) -> None:
        settings = SettingsDialog(self.page)
        self.page.dialog = settings
        settings.open = True
        await self.page.update_async()

    async def did_mount_async(self) -> None:
        await self.generate_accounts.generate()
