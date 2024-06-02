from asyncio import Event
from functools import partial
from typing import Any

import flet as ft

from ..database import SQLite
from ..components import Logout
from ..components import AccountExists
from ..components import ErrorAddAccount
from ..telegram import UserClient


class Authorization(ft.AlertDialog):
    """The class of the account telegram authorization dialog box."""
    def __init__(self, page: ft.Page, is_primary: bool, _) -> None:
        super().__init__()
        self._ = _
        self.page: ft.Page = page
        self.is_primary: bool = is_primary
        self.password_inputed_event: Event = Event()
        self.code_inputed_event: Event = Event()
        self.client: UserClient = UserClient()

        self.qrcode_image: ft.Image = ft.Image("1")

        self.log_phone_number_button: ft.TextButton = ft.TextButton()
        self.log_phone_number_button.text = _("Use phone number")
        self.log_phone_number_button.on_click = self.phone_login_dialog
        self.log_phone_number_button.disabled = False

        self.log_qrcode_button: ft.TextButton = ft.TextButton()
        self.log_qrcode_button.text = _("Use QR-code")
        self.log_qrcode_button.on_click = self.qr_login_dialog
        self.log_qrcode_button.visible = True

        self.phone_field: ft.TextField = ft.TextField()
        self.phone_field.label = _("Phone number")
        self.phone_field.prefix_text = "+"
        self.phone_field.max_length = 16
        self.phone_field.text_size = 24
        self.phone_field.input_filter = ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
        )
        self.phone_field.on_submit = self.__call_phone_auth
        self.phone_field.keyboard_type = ft.KeyboardType.PHONE
        self.phone_field.visible = False

        self.code_field: ft.TextField = ft.TextField()
        self.code_field.label = _("SMS code")
        self.code_field.max_length = 5
        self.code_field.text_size = 24
        self.code_field.input_filter = ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string=""
        )
        self.code_field.on_submit = self.__submit
        self.code_field.visible = True

        self.password = ft.TextField()
        self.password.label = _("2FA password")
        self.password.text_size = 24
        self.password.visible = True
        self.password.password = True
        self.password.autofocus = True
        self.password.on_submit = self.__submit

        self.button_close = ft.TextButton(_("Close"), on_click=self.__close)
        self.button_submit = ft.FilledButton(_("Submit"), on_click=self.__submit)
        self.button_continue = ft.TextButton(_("Continue"), on_click=self.__call_phone_auth)

        self.modal = True
        self.content = ft.Column(
            [
                self.phone_field,
                self.qrcode_image,
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
        if self.code_field in self.content.controls:
            self.code_field.read_only = True
        if self.button_submit not in self.actions:
            self.actions.append(self.button_submit)
        self.log_phone_number_button.visible = False
        self.qrcode_image.visible = False
        if self.password not in self.content.controls:
            self.content.controls.append(self.password)
        self.update()

    async def input_code(self):
        """"""
        if self.log_qrcode_button in self.actions:
            self.actions.remove(self.log_qrcode_button)
        if self.button_continue in self.actions:
            self.actions.remove(self.button_continue)
        if self.button_submit not in self.actions:
            self.actions.append(self.button_submit)
        self.phone_field.read_only = True
        if self.code_field not in self.content.controls:
            self.content.controls.append(self.code_field)
        self.update()


    async def qr_login_dialog(self, e: ft.TapEvent = None):
        """Call authorization dialog by QRCode."""
        if self.code_field in self.content.controls:
            self.content.controls.remove(self.code_field)

        if self.password in self.content.controls:
            self.content.controls.remove(self.password)

        if self.button_continue in self.actions:
            self.actions.remove(self.button_continue)

        if self.button_submit in self.actions:
            self.actions.remove(self.button_submit)

        if self.log_qrcode_button in self.actions:
            self.actions.remove(self.log_qrcode_button)

        if self.log_phone_number_button not in self.actions:
            self.actions.append(self.log_phone_number_button)

        self.phone_field.visible = False
        self.qrcode_image.visible = True
        self.update()

        result = await self.client.login_by_qrcode(
            dialog=self,
            is_primary=self.is_primary
        )
        if result == 1555:
            await self.__close()
            self.page.pubsub.send_all("update")
            AccountExists(self.page, self._)

        if result is True:
            await self.__close()
            self.page.pubsub.send_all("update")

    async def phone_login_dialog(self, e: ft.TapEvent = None):
        """Authorization dialog by phone number."""
        self.qrcode_image.visible = False
        self.phone_field.visible = True
        if self.log_phone_number_button in self.actions:
            self.actions.remove(self.log_phone_number_button)
        if self.log_qrcode_button not in self.actions:
            self.actions.append(self.log_qrcode_button)
        if self.button_continue not in self.actions:
            self.actions.append(self.button_continue)
        self.update()

    async def __call_phone_auth(self, e: ft.TapEvent):
        result = await self.client.login_by_phone_number(
            self,
            self.is_primary
        )
        if result == 1555:
            await self.__close()
            self.page.pubsub.send_all("update")
            AccountExists(self.page, self._)

        if result is True:
            await self.__close()
            self.page.pubsub.send_all("update")

    async def password_invalid(self):
        """Error style for 2fa input field."""
        self.password.border_color = ft.colors.RED
        self.password.focus()
        self.password.update()

    async def password_valid(self):
        self.password.border_color = ft.colors.GREEN
        self.password.update()

    async def phone_number_invalid(self):
        self.phone_field.border_color = ft.colors.RED
        self.phone_field.focus()
        self.phone_field.update()
    
    async def phone_number_valid(self):
        self.phone_field.border_color = ft.colors.GREEN
        self.phone_field.update()

    async def phone_code_invalid(self):
        self.code_field.border_color = ft.colors.RED
        self.code_field.focus()
        self.code_field.update()

    async def phone_code_valid(self):
        self.code_field.border_color = ft.colors.GREEN
        self.code_field.update()

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

    async def generate(self) -> None:
        """Regenerate accounts and build container."""
        accounts: list[Any] = self.database.get_users()
        while len(self.account_primary.controls) > 3:
            self.account_primary.controls.pop(-2)
        while len(self.account_secondary.controls) > 3:
            self.account_secondary.controls.pop(-2)
        for account in accounts:
            client = UserClient(account[19])
            if await client.is_user_valid():
                if bool(account[1]):
                    self.account_primary.controls.insert(
                        -1, self.account_button(account[0], account[4][0:16])
                    )
                else:
                    self.account_secondary.controls.insert(
                        -1, self.account_button(account[0], account[4][0:16])
                    )
            else:
                self.database.delete_user_by_id(account[0])
        self.update()

    def callback(self) -> None:
        """Callback query for re-generate accounts container."""
        self.page.run_task(self.generate)

    def did_mount(self):
        self.page.run_task(self.generate)
