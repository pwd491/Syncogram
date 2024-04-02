import flet as ft

class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args, **kwargs) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.update_accounts = args[0]
        # self.client = UserClient(self)

        self.qrcode_image = ft.Text()

        self.wrapper_auth_method_container = ft.Container()
        self.wrapper_auth_method_container.content = ft.Row([self.qrcode_image])
        self.wrapper = ft.Container()
        self.wrapper.width = 400
        self.wrapper.height = 400
        self.wrapper.content = ft.Column(
            [
                self.qrcode_image,
            ]
        )
        self.wrapper.content.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.modal = True
        self.content = self.wrapper
        self.title = ft.Text("Authorization")
        self.actions = [ft.TextButton("Ok", on_click=self.close)]


    def close(self, e):
        self.update_accounts()
        self.open = False
        self.update()