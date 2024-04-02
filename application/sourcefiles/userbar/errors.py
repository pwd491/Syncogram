import flet as ft

class ErrorAddAccount(ft.AlertDialog):
    def __init__(self):
        super().__init__(
            modal=True,
            title=ft.Text("Sorry 😔"),
            content=ft.Text(
                "The application does not support more than 1 account, expect in the future."
            ),
            actions=[
                ft.TextButton("Okay", on_click=self.close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def close(self, e):
        self.open = False
        self.update()