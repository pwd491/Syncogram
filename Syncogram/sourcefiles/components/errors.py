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


class AccountExists(ft.SnackBar):
    """Displaying notify account has been added early."""

    def __init__(self, page: ft.Page, _) -> None:
        self.text = ft.Text()
        self.text.value = _("This account has already been logged into the application.")
        self.text.color = ft.colors.WHITE
        self.content = self.text
        self.content.text_align = ft.TextAlign.CENTER
        super().__init__(self.content)
        self.duration = 10000
        self.bgcolor = ft.colors.BLACK87
        page.snack_bar = self
        page.snack_bar.open = True
        page.update()