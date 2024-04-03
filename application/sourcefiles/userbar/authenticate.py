from asyncio import Event

from ..telegram import UserClient

import flet as ft


class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args, **kwargs) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.client = UserClient(self)
        self.update_accounts = args[0]
        self.is_primary = args[1]
        self.password_inputed_event = Event()

        self.qrcode_image = ft.Image("1")
        
        self.password = ft.TextField()
        self.password.label = "2FA password"
        self.password.visible = False
        self.password.autofocus = True
        self.password.on_submit = self.submit


        self.modal = True
        self.content = ft.Column(
            [
                self.qrcode_image,
                self.password
            ]
        )
        self.content.width = 400
        self.content.height = 400
        self.content.alignment = ft.MainAxisAlignment.CENTER
        self.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.title = ft.Text("Authorization")
        self.actions = [ft.TextButton("Close", on_click=self.close)]

    async def submit(self, e):
        self.password_inputed_event.set()
        self.password_inputed_event.clear()

    async def did_mount_async(self):
        await self.client.login_by_qrcode(self.is_primary)
        await self.update_accounts.generate()
        await self.update_accounts.update_async()
        await self.update_async()

    async def input_2fa_password(self):
        self.qrcode_image.visible = False
        self.password.visible = True
        await self.update_async()

    async def close(self, e):
        await self.update_accounts.generate()
        self.open = False
        await self.update_async()