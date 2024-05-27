from asyncio import Event
from functools import partial
from typing import Any

import flet as ft

from ..database import SQLite
from ..components import Logout
from ..components import ErrorAddAccount
from ..telegram import UserClient


class Authorization(ft.AlertDialog):
    """The class of the account telegram authorization dialog box."""
    def __init__(self, page: ft.Page, is_primary: bool, _) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.is_primary: bool = is_primary
        self.password_inputed_event: Event = Event()
        self.client: UserClient = UserClient()

        self.qrcode_image: ft.Image = ft.Image("1")

        self.log_phone_number_button: ft.TextButton = ft.TextButton()
        self.log_phone_number_button.text = _("Use phone number")
        self.log_phone_number_button.on_click = self.phone_login_dialog
        self.log_phone_number_button.disabled = True
        self.log_phone_number_button.tooltip = _("It will available in next updates")

        self.log_qrcode_button: ft.TextButton = ft.TextButton()
        self.log_qrcode_button.text = _("Use QR-code")
        self.log_qrcode_button.on_click = self.qr_login_dialog
        self.log_qrcode_button.visible = False

        self.phone_text: ft.Text = ft.Text()
        self.phone_text.value = "Введите номер телефона"
        self.phone_field: ft.TextField = ft.TextField()
        self.phone_field.keyboard_type = ft.KeyboardType.PHONE
        self.phone_field.visible = False

        self.password = ft.TextField()
        self.password.label = _("2FA password")
        self.password.visible = False
        self.password.password = True
        self.password.autofocus = True
        self.password.on_submit = self.__submit

        self.button_close = ft.TextButton(_("Close"), on_click=self.__close)
        self.button_submit = ft.FilledButton(_("Submit"), on_click=self.__submit)

        self.modal = True
        self.content = ft.Column(
            [
                self.phone_field,
                self.qrcode_image,
                self.password
            ]
        )
        self.content.width = 400
        self.content.height = 400
        self.content.alignment = ft.MainAxisAlignment.CENTER
        self.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.title = ft.Text(_("Authorization"))
        self.actions = [
            self.button_close,
            self.log_phone_number_button,

        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    async def __close(self, e: ft.TapEvent = None):
        """Close dialog."""
        if self.client.is_connected():
            await self.client.disconnect()
        self.open = False
        self.page.dialog.clean()
        self.update()

    async def __submit(self, e):
        """Event for submit 2FA password."""
        self.password_inputed_event.set()
        self.password_inputed_event.clear()

    async def input_2fa_password(self):
        """Create input 2FA password and display."""
        self.actions.append(self.button_submit)
        self.log_phone_number_button.visible = False
        self.qrcode_image.visible = False
        self.password.visible = True
        self.update()

    async def qr_login_dialog(self, e: ft.TapEvent = None):
        """Call authorization dialog by QRCode."""
        if self.log_qrcode_button in self.actions:
            self.actions.pop(-1)
        if self.log_phone_number_button not in self.actions:
            self.actions.append(self.log_phone_number_button)   
        self.phone_field.visible = False
        self.qrcode_image.visible = True
        self.update()
        await self.client.login_by_qrcode(
            dialog=self,
            is_primary=self.is_primary
        )
        await self.__close()
        # Need to except 1555 error UNIQUE ID PRIMARY KEY (user exists.)
        self.page.pubsub.send_all("update")

    async def phone_login_dialog(self, e):
        """Authorization dialog by phone number."""
        self.qrcode_image.visible = False
        self.phone_field.visible = True
        if self.log_phone_number_button in self.actions:
            self.actions.pop(-1)
        if self.log_qrcode_button not in self.actions:
            self.actions.append(self.log_qrcode_button)
        self.update()
    
    async def error(self):
        """Error style for 2fa input field."""
        self.password.border_color = ft.colors.RED
        self.password.focus()
        self.password.update()

    async def manager(self):
        await self.qr_login_dialog()

    def did_mount(self):
        self.page.run_task(self.manager)


class Accounts(ft.Container):
    """Generate accounts container side."""
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.database: SQLite = SQLite()
        self.client: UserClient = UserClient()
        self._ = _

        self.divider = ft.Container()
        self.divider.width = 200
        self.divider.height = 0.5
        self.divider.border_radius = ft.BorderRadius(5,5,5,5)
        self.divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER

        self.account_primary = ft.Column()
        self.account_primary.controls = [
            ft.Row([self.label(self._("From:"))]),
            ft.Row([self.divider]),
            ft.Row([self.add_button(True)]),
        ]

        self.account_secondary = ft.Column()
        self.account_secondary.controls = [
            ft.Row([self.label(self._("Where:"))]),
            ft.Row([self.divider]),
            ft.Row([self.add_button(False)]),
        ]

        self.wrapper_column = ft.Column()
        self.wrapper_column.controls = [
            self.account_primary,
            self.account_secondary
        ]

        self.content = self.wrapper_column
        self.callback()

    def account_button(self, account_id, account_name) -> ft.ElevatedButton:
        """Clickable user button."""
        button = ft.ElevatedButton()
        button.width = 250
        button.height = 35
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.bgcolor = ft.colors.SECONDARY_CONTAINER
        button.key = account_id
        button.on_click = partial(self.logout, account_id=button.key)
        return button

    def add_button(self, is_primary: bool) -> ft.OutlinedButton:
        """Create button to add account."""
        button = ft.OutlinedButton()
        button.height = 35
        button.text = self._("Add account")
        button.icon = ft.icons.ADD
        button.expand = True
        button.data = is_primary
        button.on_click = partial(self.add_account, is_primary=button.data)
        return button

    def label(self, text: str) -> ft.Text:
        """Creating label."""
        label = ft.Text()
        label.value = text
        label.size = 11
        label.opacity = .5
        return label

    async def logout(self, e, account_id):
        """Opening logout dialog."""
        dialog = Logout(self.page, account_id, self._)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    async def add_account(self, e, is_primary: bool):
        """Open authorization dialog or show error."""
        accounts: list[Any] = self.database.get_users()
        for acc in accounts:
            if int(is_primary) == acc[1]:
                ErrorAddAccount(self.page, self._)
                return
        authorization = Authorization(self.page, is_primary, self._)
        self.page.dialog = authorization
        authorization.open = True
        self.page.update()

    def callback(self) -> None:
        """Regenerate accounts and build container."""
        accounts: list[Any] = self.database.get_users()
        while len(self.account_primary.controls) > 3:
            self.account_primary.controls.pop(-2)
        while len(self.account_secondary.controls) > 3:
            self.account_secondary.controls.pop(-2)
        for account in accounts:
            if bool(account[1]):
                self.account_primary.controls.insert(
                    -1, self.account_button(account[0], account[4][0:16])
                )
            else:
                self.account_secondary.controls.insert(
                    -1, self.account_button(account[0], account[4][0:16])
                )
