from functools import partial
from typing import Any
from sql import SQLite
import flet as ft


class Navbar(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.database = SQLite()

        # Labels
        # [from]
        self.navbar_wrapper_from_label = ft.Text()
        self.navbar_wrapper_from_label.value = "From:"
        self.navbar_wrapper_from_label.size = 11
        self.navbar_wrapper_from_label.opacity = 0.5
        # [where]
        self.navbar_wrapper_where_label = ft.Text()
        self.navbar_wrapper_where_label.value = "Where:"
        self.navbar_wrapper_where_label.size = 11
        self.navbar_wrapper_where_label.opacity = 0.5


        # Buttons
        self.settings_btn = ft.ElevatedButton()
        self.settings_btn.text = "Settings"
        self.settings_btn.icon = ft.icons.SETTINGS
        self.settings_btn.expand = True
        self.settings_btn.height = 45


        # Fields
        self.name_field = ft.TextField()
        self.name_field.label = "Name"


        # Divider
        self.navbar_wrapper_divider = ft.Container()
        self.navbar_wrapper_divider.width = 200
        self.navbar_wrapper_divider.height = 0.5
        self.navbar_wrapper_divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER


        # Containers

        # [Major block to display accounts on navbar]
        self.navbar_wrapper_accounts_side = ft.Container()
        self.navbar_wrapper_accounts_side.content = ft.Column([
            self.ui_generate_account_container("primary"),
            self.ui_generate_account_container("secondary"),
        ])


        # [Settings into bottom menu]
        self.navbar_wrapper_settings = ft.Container(ft.Row([self.settings_btn]))
        self.navbar_wrapper_settings.width = 200
        self.navbar_wrapper_settings.height = 50


        # Main block like canvas to display controls
        self.navbar_wrapper = ft.Container()
        self.navbar_wrapper.content = ft.Column([
            self.navbar_wrapper_accounts_side,
            self.navbar_wrapper_settings,
        ])
        self.navbar_wrapper.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.navbar_wrapper.width = 250
        self.navbar_wrapper.padding = 20
        self.navbar_wrapper.content.expand = True
        self.navbar_wrapper.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.navbar_wrapper.bgcolor = ft.colors.SECONDARY_CONTAINER


    def ui_account_button(self, account_id, account_name):
        button = ft.ElevatedButton()
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.expand = True
        button.key = account_id
        button.on_click = ...
        return button

    def ui_add_account_button(self, key):
        button = ft.OutlinedButton()
        button.text = "Add account"
        button.icon = ft.icons.ADD
        button.expand = True
        button.key = key
        button.on_click = partial(self.ui_add_account, key=button.key)
        return button


    def ui_add_account(self, e, key):
        print(key)


    def ui_generate_account_container(self, status):
        accounts: list[Any] = self.database.get_accounts()
        print(accounts, type(accounts))

        navbar_wrapper_account_container = ft.Column()
        navbar_wrapper_account_container.key = status
        navbar_wrapper_account_container.width = 200
        navbar_wrapper_account_container.controls = []

        if not bool(len(accounts)):
            pass


        if status == "primary":
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.navbar_wrapper_from_label]),
            )
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.navbar_wrapper_divider]),
            )
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.ui_add_account_button("primary")]),
            )
            for account in accounts:
                if bool(account[2]) is True:
                    navbar_wrapper_account_container.controls.insert(
                        -1, ft.Row([self.ui_account_button(
                            account_id=account[0],
                            account_name=account[1],
                        )]),
                    )
                    break
        else:
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.navbar_wrapper_where_label]),
            )
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.navbar_wrapper_divider]),
            )
            navbar_wrapper_account_container.controls.append(
                ft.Row([self.ui_add_account_button("secondary")]),
            )
            for account in accounts:
                if bool(account[2]) is False:
                    navbar_wrapper_account_container.controls.insert(
                        -1, ft.Row([self.ui_account_button(
                            account_id=account[0],
                            account_name=account[1]
                        )]),
                    )
                    break
        
        return navbar_wrapper_account_container

    def build(self):
        return self.navbar_wrapper


def application(page: ft.Page):
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.Row([Navbar(page)], expand=True)
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
