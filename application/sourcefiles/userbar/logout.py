import flet as ft
from telethon.sessions import StringSession

from ..telegram import UserClient
from ..database import SQLite

class LogOutDialog(ft.AlertDialog):
    def __init__(self, account_id, *args) -> None:
        super().__init__()
        self.database = SQLite()
        self.account_id = account_id
        self.update_accounts = args[0]
        self.update_mainwindow = args[1]

        self.modal = False
        self.title = ft.Text("Are you sure to logout?")
        self.title.size = 13
        self.title.text_align = ft.TextAlign.CENTER
        # self.bgcolor = ft.colors.TRANSPARENT
        self.actions = [
            ft.FilledButton("Yes", on_click=self.submit),
            ft.TextButton("No", on_click=self.close),
        ]
        self.actions_alignment = ft.MainAxisAlignment.CENTER

    async def submit(self, e) -> None:
        session = self.database.get_user_by_id(self.account_id)
        client = UserClient(*session)
        if await client.logout():
            self.database.delete_user_by_id(self.account_id)

        self.open = False
        await self.update_accounts()
        await self.update_mainwindow()
        await self.update_async()


    async def close(self, e):
        self.open = False
        await self.update_mainwindow()
        await self.update_async()
