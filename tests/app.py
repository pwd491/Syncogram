from functools import partial
from typing import Any
from sql import SQLite
import flet as ft

class Section(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.section = ft.Column([ft.Text('asd')])
        
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

        self.wrapper_qrcode = ft.Container()
        self.wrapper_qrcode.content = ft.Row()
        self.wrapper_qrcode.height = 20
        self.wrapper_qrcode.bgcolor = 'yellow'

        self.wrapper = ft.Container()
        self.wrapper.width = 400
        self.wrapper.height = 400
        self.wrapper.content = ft.Column([self.wrapper_qrcode])
        self.wrapper.bgcolor = 'red'

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


        # Labels
        ### Нужно переделать !!!
        self.wrapper_from_label = ft.Text()
        self.wrapper_from_label.value = "From:"
        self.wrapper_from_label.size = 11
        self.wrapper_from_label.opacity = 0.5

        self.wrapper_where_label = ft.Text()
        self.wrapper_where_label.value = "Where:"
        self.wrapper_where_label.size = 11
        self.wrapper_where_label.opacity = 0.5


        # Buttons
        self.add_primary_button = ft.OutlinedButton()
        self.add_primary_button.text = "Add account"
        self.add_primary_button.icon = ft.icons.ADD
        self.add_primary_button.expand = True
        self.add_primary_button.key = "primary"
        self.add_primary_button.on_click = partial(
            self.ui_add_account_process,
            status=self.add_primary_button.key
        )

        self.add_secondary_button = ft.OutlinedButton()
        self.add_secondary_button.text = "Add account"
        self.add_secondary_button.icon = ft.icons.ADD
        self.add_secondary_button.expand = True
        self.add_secondary_button.key = "secondary"
        self.add_secondary_button.on_click = partial(
            self.ui_add_account_process,
            status=self.add_secondary_button.key
        )

        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        self.settings_btn.height = 45


        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"

        # CustomAlertDialog
        self.window_authentication = AuthenticationDialogProcedure(
            self.page,
            self.ui_generate_accounts,
        )

        # Divider
        self.divider = ft.Container()
        self.divider.width = 200
        self.divider.height = 0.5
        self.divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER


        # Containers
        ### [Major block to display accounts on navbar]

        # [Account container `WHERE`]
        self.wrapper_account_primary = ft.Column()
        self.wrapper_account_primary.controls = [
            ft.Row([self.wrapper_from_label]),
            ft.Row([self.divider]),
            ft.Row([self.add_primary_button]),
        ]

        self.wrapper_account_secondary = ft.Column()
        self.wrapper_account_secondary.controls = [
            ft.Row([self.wrapper_where_label]),
            ft.Row([self.divider]),
            ft.Row([self.add_secondary_button]),
        ]


        self.wrapper_accounts_side = ft.Container()
        self.wrapper_accounts_side.content = ft.Column([
            self.wrapper_account_primary,
            self.wrapper_account_secondary,
        ])



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

    def ui_account_button(self, account_id, account_name) -> ft.ElevatedButton:
        button = ft.ElevatedButton()
        button.width = 250
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.key = account_id
        button.on_click = ...
        return button


    def ui_generate_accounts(self):
        accounts: list[Any] = self.database.get_accounts()
        self.wrapper_account_primary.clean()
        self.wrapper_account_secondary.clean()
        for account in accounts:
            if bool(account[2]):
                self.wrapper_account_primary.controls.insert(
                    -1, self.ui_account_button(account[0], account[1])
                )
            else:
                self.wrapper_account_secondary.controls.insert(
                    -1, self.ui_account_button(account[0], account[1])
                )
        self.update()


    def ui_add_account_process(self, e, status):
        accounts: list[Any] = self.database.get_accounts()

        self.page.dialog = self.window_authentication
        self.window_authentication.open = True
        self.page.update()



def application(page: ft.Page) -> None:
    page.add(
        ft.Row([
            UserBar(page),
            Section(page),
        ], expand=True)
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
