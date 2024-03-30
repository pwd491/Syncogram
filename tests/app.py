from functools import partial
from typing import Any
from sql import SQLite
import flet as ft

class Section(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.sticker = ft.Image()
        self.sticker.src = "/home/admin/Development/Syncogram/application/assets/sticker.gif"
        self.sticker.width = 350

        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")
        
        self.section = ft.Column([self.sticker, self.sticker_text])
        self.section.alignment = ft.MainAxisAlignment.CENTER
        self.section.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        super().__init__(
            self.section,
            expand=True,
            bgcolor = ft.colors.SECONDARY_CONTAINER,
            border_radius = ft.BorderRadius(10, 10, 10, 10),
            padding=20
        )



class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args, **kwargs) -> None:
        self.page: ft.Page = page
        self.update_accounts = args[0]
        self.wrapper_telephone = ft.Container()

        self.qrcode_image = ft.Image("/home/admin/Development/Syncogram/tests/qrtest.png")
        self.qrcode_image.expand = True


        self.wrapper_auth_method_container = ft.Container()
        self.wrapper_auth_method_container.content = ft.Row([self.qrcode_image])

        self.wrapper = ft.Container()
        self.wrapper.width = 400
        self.wrapper.height = 400
        self.wrapper.content = ft.Column([self.wrapper_auth_method_container])
        # self.wrapper.bgcolor = 'red'

        super().__init__(
            modal=True,
            title=ft.Text("Authentication via Telegram"),
            content=self.wrapper,
            actions=[
                ft.TextButton("Ok", on_click=self.close)
            ],
        )

    def close(self, e):
        self.update_accounts()
        self.open = False
        self.update()


class UserBar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.database = SQLite()
        self.page: ft.Page = page
        self.UIGenerateAccounts = UIGenerateAccounts(page, self.ui_add_account_process)
        

        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        self.settings_btn.height = 45


        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"

        self.wrapper_accounts_side: UIGenerateAccounts = self.UIGenerateAccounts
        # CustomAlertDialog
        self.window_authentication = AuthenticationDialogProcedure(
            self.page,
            self.UIGenerateAccounts.generate
        )

        # Containers
        # [Settings into bottom menu]
        self.wrapper_settings = ft.Container(ft.Row([self.settings_btn]))
        self.wrapper_settings.width = 200
        self.wrapper_settings.height = 50


        # Main block like canvas to display controls
        self.wrapper = ft.Container()
        self.wrapper.content = ft.Column([
            self.wrapper_accounts_side,
            self.wrapper_settings,
        ])
        self.wrapper.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.wrapper.width = 250
        self.wrapper.padding = 20
        self.wrapper.content.expand = True
        self.wrapper.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.wrapper.bgcolor = ft.colors.SECONDARY_CONTAINER

        super().__init__(self.wrapper)

    def did_mount(self):
        self.UIGenerateAccounts.generate()

    def ui_add_account_process(self, e, status):
        accounts: list[Any] = self.database.get_accounts()
        
        self.page.dialog = self.window_authentication
        self.window_authentication.open = True
        self.page.update()


class UIGenerateAccounts(ft.UserControl):
    def __init__(self, page: ft.Page, *args):
        self.database = SQLite()
        self.page: ft.Page = page

        self.process_func = args[0]

        self.divider = ft.Container()
        self.divider.width = 200
        self.divider.height = 0.5
        self.divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER


        self.account_primary = ft.Column()
        self.account_primary.controls = [
            ft.Row([self.label("From:")]),
            ft.Row([self.divider]),
            ft.Row([self.add_button("primary")]),
        ]

        self.account_secondary = ft.Column()
        self.account_secondary.controls = [
            ft.Row([self.label("Where:")]),
            ft.Row([self.divider]),
            ft.Row([self.add_button("secondary")]),
        ]

        self.wrapper_column = ft.Column()
        self.wrapper_column.controls = [
            self.account_primary,
            self.account_secondary
        ]

        self.wrapper = ft.Container()
        self.wrapper.content = self.wrapper_column

        super().__init__()

    def account_button(self, account_id, account_name) -> ft.ElevatedButton:
        button = ft.ElevatedButton()
        button.width = 250
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.key = account_id
        button.on_click = ...
        return button

    def add_button(self, key: str) -> ft.OutlinedButton:
        button = ft.OutlinedButton()
        button.text = "Add account"
        button.icon = ft.icons.ADD
        button.expand = True
        button.key = key
        button.on_click = partial(self.process_func, button.key)
        return button

    def label(self, text: str) -> ft.Text:
        label = ft.Text()
        label.value = text
        label.size = 11
        label.opacity = 0.5
        return label

    def generate(self):
        accounts = self.database.get_accounts()
        while len(self.account_primary.controls) > 3:
            self.account_primary.controls.pop(-2)
        while len(self.account_secondary.controls) > 3:
            self.account_secondary.controls.pop(-2)
        for account in accounts:
            if bool(account[2]):
                self.account_primary.controls.insert(
                    -1, self.account_button(account[0], account[1])
                )
            else:
                self.account_secondary.controls.insert(
                    -1, self.account_button(account[0], account[1])
                )
        self.update()

    def build(self) -> ft.Container:
        return self.wrapper


def application(page: ft.Page) -> None:
    # page.theme_mode = ft.ThemeMode.LIGHT

    page.theme = ft.Theme()

    page.add(
        ft.Row([
            UserBar(page),
            Section(page),
        ], expand=True)
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
