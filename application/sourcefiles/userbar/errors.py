import flet as ft

class ErrorAddAccount(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.modal=False
        self.title= ft.Text("Sorry 😔")
        self.content = ft.Text(
            "The application does not support more than 1 account, expect in the future."
        )
        self.actions = [
            ft.TextButton("Okay", on_click=self.close)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    async def close(self, e):
        self.open = False
        await self.update_async()
