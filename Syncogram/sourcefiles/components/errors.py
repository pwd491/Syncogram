import flet as ft

class ErrorAddAccount(ft.AlertDialog):
    def __init__(self, page: ft.Page, _) -> None:
        super().__init__()
        self.page = page

        self.modal=False
        self.title= ft.Text(_("Sorry 😔"))
        self.content = ft.Text(
            _("The application does not support more than 1 account, expect in the future.")
        )
        self.actions = [
            ft.TextButton(_("Okay"), on_click=self.__close)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

        self.page.dialog = self
        self.open = True
        self.page.update()

    async def __close(self, e) -> None:
        self.open = False
        self.page.dialog.clean()
        self.update()
