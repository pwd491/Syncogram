import flet as ft

from .about import AboutApplication
from .about import FeedBack
from .settings import SettingsDialog
from .generate import UIGenerateAccounts
from ..database import SQLite


class UserBar(ft.Container):
    def __init__(self, page: ft.Page, update_mainwin) -> None:
        super().__init__()
        self.database = SQLite()
        self.page: ft.Page = page
        self.update_mainwin = update_mainwin
        self.generate_accounts = UIGenerateAccounts(self.page, self.update_mainwin)
        self.about = AboutApplication()

        # Buttons
        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        # self.settings_btn.width = 200
        self.settings_btn.height = 45
        self.settings_btn.on_click = self.settings

        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"

        # Containers
        self.wrapper_accounts_side: UIGenerateAccounts = self.generate_accounts

        self.wrapper_settings = ft.Row([self.settings_btn])
        self.wrapper_about = ft.Row([self.about], alignment=ft.MainAxisAlignment.CENTER)

        self.upper = ft.Column(
            [
                FeedBack(),
                self.wrapper_about,
                ft.Divider(opacity=0.3),
                self.wrapper_settings,
            ]
        )

        # Main block like canvas to display controls
        self.content = ft.Column(
            [
                self.wrapper_accounts_side,
                self.upper
            ]
        )
        self.width = 250
        self.padding = 20
        self.content.expand = True
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def settings(self, e) -> None:
        settings = SettingsDialog(self.update_mainwin)
        self.page.dialog = settings
        settings.open = True
        await self.page.update_async()

    async def did_mount_async(self) -> None:
        await self.generate_accounts.generate()
