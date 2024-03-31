from utils import clr_on_secondary_container, clr_secondary_container
from functools import partial
from typing import Any
from sql import SQLite
import flet as ft


class Section(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.sticker = ft.Image()
        self.sticker.src = "D:\\Developer\\Syncogram\\application\\assets\\sticker2.gif"
        self.sticker.width = 200

        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")

        self.wrapper =  ft.Column([self.sticker, self.sticker_text])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER


        super().__init__(
            self.wrapper,
            expand=True,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER),
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=20,
        )


class AuthenticationDialogProcedure(ft.AlertDialog):
    def __init__(self, page: ft.Page, *args, **kwargs) -> None:
        self.page: ft.Page = page
        self.update_accounts = args[0]
        self.wrapper_telephone = ft.Container()

        self.qrcode_image = ft.Image(
            "qrtest.png"
        )
        self.qrcode_image.fit = ft.ImageFit.FIT_WIDTH

        self.wrapper_auth_method_container = ft.Container()
        self.wrapper_auth_method_container.content = ft.Row([self.qrcode_image])

        # self.wrapper_auth_alternative = ft.Text("or")

        # self.wrapper_button_phone_login = ft.TextButton("Phone number")

        self.wrapper = ft.Container()
        self.wrapper.width = 400
        self.wrapper.height = 400
        # self.wrapper.bgcolor = "red"
        self.wrapper.content = ft.Column(
            [
                self.qrcode_image,
                # self.wrapper_auth_alternative,
                # self.wrapper_button_phone_login
            ]
        )
        self.wrapper.content.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        super().__init__(
            modal=True,
            title=ft.Text("Authorization"),
            content=self.wrapper,
            actions=[ft.TextButton("Ok", on_click=self.close)],
        )

    def close(self, e):
        self.update_accounts()
        self.open = False
        self.update()


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


class SettingsDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.database = SQLite()
        """Подумай над этим блоком"""
        self.options = self.database.get_options()
        self.options = self.options if not None else (0, 0, 0)

        self.c1 = ft.Checkbox(label="Sync my favorite messages", value=False)
        self.c2 = ft.Checkbox(
            label="Save the sequence of pinned messages", value=False, disabled=True
        )
        """Подумай над этим блоком"""
        self.column = ft.Container()
        self.column.content = ft.Column([self.c1, self.c2])
        self.column.height = 350

        self.wrapper = ft.Container()
        self.wrapper.content = self.column

        super().__init__(
            modal=True,
            title=ft.Row([ft.Icon("SETTINGS"), ft.Text("Settings")]),
            content=self.wrapper,
            actions=[
                ft.TextButton("Cancel", on_click=self.close),
                ft.TextButton("Save", on_click=self.save),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def close(self, e):
        self.open = False
        self.update()

    def save(self, e):
        self.database.set_options(int(self.c1.value), int(self.c2.value))
        self.open = False
        self.update()


class UserBar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.database = SQLite()
        self.page: ft.Page = page
        self.UIGenerateAccounts = UIGenerateAccounts(page, self.ui_add_account_process)

        # Buttons
        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        self.settings_btn.height = 45
        self.settings_btn.on_click = self.settings

        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"

        # CustomAlertDialog
        self.error_add_account_dialog = ErrorAddAccount()
        self.settings_dialog = SettingsDialog(page)

        self.window_authentication = AuthenticationDialogProcedure(
            self.page, self.UIGenerateAccounts.generate
        )

        # Containers
        self.wrapper_accounts_side: UIGenerateAccounts = self.UIGenerateAccounts

        self.wrapper_settings = ft.Container(ft.Row([self.settings_btn]))
        self.wrapper_settings.width = 200
        self.wrapper_settings.height = 50

        # Main block like canvas to display controls
        self.wrapper = ft.Container()
        self.wrapper.content = ft.Column(
            [
                self.wrapper_accounts_side,
                self.wrapper_settings,
            ]
        )
        self.wrapper.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.wrapper.width = 250
        self.wrapper.padding = 20
        self.wrapper.content.expand = True
        self.wrapper.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.wrapper.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)

        super().__init__(self.wrapper)

    def did_mount(self):
        self.UIGenerateAccounts.generate()

    def ui_add_account_process(self, e, is_primary: bool):
        accounts: list[Any] = self.database.get_users()
        for acc in accounts:
            if int(is_primary) == acc[2]:
                self.page.dialog = self.error_add_account_dialog
                self.error_add_account_dialog.open = True
                self.UIGenerateAccounts.generate()
                self.page.update()
                return

        self.page.dialog = self.window_authentication
        self.window_authentication.open = True
        self.page.update()

    def settings(self, e):
        self.page.dialog = self.settings_dialog
        self.settings_dialog.open = True
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
            ft.Row([self.add_button(True)]),
        ]

        self.account_secondary = ft.Column()
        self.account_secondary.controls = [
            ft.Row([self.label("Where:")]),
            ft.Row([self.divider]),
            ft.Row([self.add_button(False)]),
        ]

        self.wrapper_column = ft.Column()
        self.wrapper_column.controls = [self.account_primary, self.account_secondary]

        self.wrapper = ft.Container()
        self.wrapper.content = self.wrapper_column

        super().__init__()

    def account_button(self, account_id, account_name) -> ft.ElevatedButton:
        button = ft.ElevatedButton()
        button.width = 250
        button.height = 35
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.bgcolor = ft.colors.SECONDARY_CONTAINER
        button.key = account_id
        button.on_click = ...
        return button

    def add_button(self, key: bool) -> ft.OutlinedButton:
        button = ft.OutlinedButton()
        button.height = 35
        button.text = "Add account"
        button.icon = ft.icons.ADD
        button.expand = True
        button.data = key
        button.on_click = partial(self.process_func, is_primary=button.data)
        return button

    def label(self, text: str) -> ft.Text:
        label = ft.Text()
        label.value = text
        label.size = 11
        label.opacity = 0.5
        return label

    def generate(self):
        accounts = self.database.get_users()
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

    # clr1 = ft.colors.SECONDARY_CONTAINER
    # clr2 = ft.colors.ON_SECONDARY_CONTAINER

    # page.dark_theme = ft.Theme(
    #     color_scheme=ft.ColorScheme(
    #         secondary_container=ft.colors.with_opacity(0.1, clr1),
    #         on_secondary_container=ft.colors.with_opacity(0.2, clr2),
    #     )
    # )

    page.add(
        ft.Row(
            [
                UserBar(page),
                Section(page),
            ],
            expand=True,
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
