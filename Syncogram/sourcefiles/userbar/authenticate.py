from asyncio import Event

from ..telegram import UserClient

import flet as ft


class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, _, *args, **kwargs) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.update_accounts = args[0]
        self.is_primary = args[1]
        self.update_mainwindow = args[2]
        self.password_inputed_event = Event()
        self.client = UserClient()


        self.qrcode_image = ft.Image("1")

        self.log_phone_number_button = ft.TextButton()
        self.log_phone_number_button.text = _("Use phone number")
        self.log_phone_number_button.on_click = self.phone_login_dialog
        self.log_phone_number_button.disabled = True

        self.log_qrcode_button = ft.TextButton()
        self.log_qrcode_button.text = _("Use QR-code")
        self.log_qrcode_button.on_click = ...
        self.log_qrcode_button.visible = False


        self.phone_field = ft.TextField()
        self.phone_field.keyboard_type = ft.KeyboardType.PHONE
        self.phone_field.visible = False


        self.password = ft.TextField()
        self.password.label = _("2FA password")
        self.password.visible = False
        self.password.autofocus = True
        self.password.on_submit = self.submit

        self.button_close = ft.TextButton(_("Close"), on_click=self.close)
        self.button_submit = ft.FilledButton(_("Submit"), on_click=self.submit)

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
        self.actions = [self.button_close, self.log_phone_number_button, self.log_qrcode_button]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    async def close(self, e):
        await self.update_accounts.generate()
        await self.update_mainwindow()
        self.open = False
        self.update()
    
    async def submit(self, e):
        self.password_inputed_event.set()
        self.password_inputed_event.clear()

    async def input_2fa_password(self):
        self.actions.append(self.button_submit)
        self.log_phone_number_button.visible = False
        # self.log_qrcode_button.visible = True
        self.qrcode_image.visible = False
        self.password.visible = True
        self.update()

    async def qr_login_dialog(self):
        await self.client.login_by_qrcode(dialog=self, is_primary=self.is_primary)
        # Need to except 1555 error UNIQUE ID PRIMARY KEY (user exists.)
        await self.update_mainwindow()
        await self.update_accounts.generate()
        await self.update_accounts.update_async()
        self.update()

    async def phone_login_dialog(self, e):
        self.client.disconnect()
        self.qrcode_image.visible = False
        self.log_qrcode_button.visible = True
        self.log_phone_number_button.visible = False
        self.phone_field.visible = True
        self.update()

    async def error(self):
        self.password.border_color = ft.colors.RED
        self.password.focus()
        self.password.update()

    def did_mount(self):
        self.page.run_task(self.qr_login_dialog)
