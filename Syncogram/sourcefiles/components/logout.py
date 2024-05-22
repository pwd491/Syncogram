import flet as ft

from ..telegram import UserClient
from ..database import SQLite

class Logout(ft.AlertDialog):
    """Logout dialog class."""
    def __init__(self, page: ft.Page, account_id, _) -> None:
        super().__init__()
        self.database = SQLite()
        self.page = page
        self.account_id = account_id

        self.title = ft.Text(_("Are you sure to logout?"))
        self.title.size = 13
        self.title.text_align = ft.TextAlign.CENTER

        self.actions = [
            ft.FilledButton(_("Yes"), on_click=self.submit),
            ft.TextButton(_("No"), on_click=self.close),
        ]
        self.actions_alignment = ft.MainAxisAlignment.CENTER
        self.modal = False

    async def submit(self, e) -> None:
        """Logout session and delete user from database."""
        session = self.database.get_session_by_id(self.account_id)
        client = UserClient(session)
        if await client.logout():
            self.database.delete_user_by_id(self.account_id)

        self.open = False
        self.page.pubsub.send_all("update")
        self.update()


    async def close(self, e):
        """Close dialog."""
        self.open = False
        self.update()
