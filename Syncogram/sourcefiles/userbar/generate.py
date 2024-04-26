from typing import Any
from functools import partial

import flet as ft

from .errors import ErrorAddAccount
from .logout import LogOutDialog
from .authenticate import AuthenticationDialogProcedure
from ..database import SQLite


class UIGenerateAccounts(ft.Container):
    def __init__(self, page: ft.Page, _, *args, **kwargs) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.database = SQLite()
        self._ = _
        self.update_mainwindow = args[0]

        self.divider = ft.Container()
        self.divider.width = 200
        self.divider.height = 0.5
        self.divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER

        self.account_primary = ft.Column()
        self.account_primary.controls = [
            ft.Row([self.label(("From:"))]),
            ft.Row([self.divider]),
            ft.Row([self.add_button(True)]),
        ]

        self.account_secondary = ft.Column()
        self.account_secondary.controls = [
            ft.Row([self.label(("Where:"))]),
            ft.Row([self.divider]),
            ft.Row([self.add_button(False)]),
        ]

        self.wrapper_column = ft.Column()
        self.wrapper_column.controls = [self.account_primary, self.account_secondary]

        # self.wrapper = ft.Container()
        # self.wrapper.content = self.wrapper_column

        self.content = self.wrapper_column

    def account_button(self, account_id, account_name) -> ft.ElevatedButton:
        button = ft.ElevatedButton()
        button.width = 250
        button.height = 35
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.bgcolor = ft.colors.SECONDARY_CONTAINER
        button.key = account_id
        button.on_click = partial(self.logout, account_id=button.key)
        return button

    def add_button(self, key: bool) -> ft.OutlinedButton:
        button = ft.OutlinedButton()
        button.height = 35
        button.text = self._("Add account")
        button.icon = ft.icons.ADD
        button.expand = True
        button.data = key
        button.on_click = partial(self.add_account, is_primary=button.data)
        return button

    def label(self, text: str) -> ft.Text:
        label = ft.Text()
        label.value = self._(text)
        label.size = 11
        label.opacity = 0.5
        return label

    async def logout(self, e, account_id):
        dialog = LogOutDialog(account_id, self._, self.generate, self.update_mainwindow)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    async def add_account(self, e, is_primary: bool):
        accounts: list[Any] = self.database.get_users()
        for acc in accounts:
            if int(is_primary) == acc[2]:
                error = ErrorAddAccount(self._)
                self.page.dialog = error
                error.open = True
                await self.generate()
                await self.update_mainwindow()
                return self.page.update()

        auth = AuthenticationDialogProcedure(self.page, self._, self, is_primary, self.update_mainwindow)
        self.page.dialog = auth
        auth.open = True
        self.page.update()


    async def generate(self) -> None:
        accounts: list[Any] = self.database.get_users()
        while len(self.account_primary.controls) > 3:
            self.account_primary.controls.pop(-2)
        while len(self.account_secondary.controls) > 3:
            self.account_secondary.controls.pop(-2)
        for account in accounts:
            if bool(account[2]):
                self.account_primary.controls.insert(
                    -1, self.account_button(account[0], account[1])
                )
            else:
                self.account_secondary.controls.insert(
                    -1, self.account_button(account[0], account[1])
                )
        self.update()

    def build(self) -> ft.Container:
        return self
