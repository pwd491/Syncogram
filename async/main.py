from functools import partial
import flet as ft
from client import UserClient

class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args, **kwargs) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.client = UserClient(self)

        self.wrapper = ft.Container()
        self.wrapper.content = ft.Image()
        self.wrapper.width = 400
        self.wrapper.height = 400


        self.modal = True
        self.title = ft.Text("Authorization")
        self.content = self.wrapper
        self.actions = [ft.TextButton("Ok", on_click=self.close)]

        self.snack_bar = ft.SnackBar(
            content=ft.Text("Success login!"),
            action="Alright!",
        )

        
    async def clear(self, e):
        self.wrapper.content = ft.TextField(label="2FA password")
        await self.update_async()


    async def auth2fa(self, function):
        self.wrapper.content = ft.TextField(label="2FA password")
        await self.update_async()
        async def call(e):
            await function(password=self.wrapper.content.value)
        self.actions.append(ft.TextButton("Login", on_click=call))
        self.wrapper.content.on_submit = call
        await self.update_async()


    async def did_mount_async(self):
        user = await self.client.login_by_qrcode()
        # user = await self.auth2fa()
        # print(user)
        await self.update_async()

    async def close(self, e):
        self.open = False
        self.client.disconnect()
        await self.update_async()

async def main(page: ft.Page) -> None:
    x = AuthenticationDialogProcedure(page)

    async def open(e):
        page.dialog = x
        x.open = True
        await page.update_async()
        
    button = ft.TextButton("Auth", on_click=open)

    await page.add_async(button)

ft.app(main)