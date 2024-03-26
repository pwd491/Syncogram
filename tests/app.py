from sql import SQLite
import flet as ft


class Navbar(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.database = SQLite()

        # Labels
        self.navbar_wrapper_from_label = ft.Text()
        self.navbar_wrapper_from_label.value = "From:"
        self.navbar_wrapper_from_label.size = 11
        self.navbar_wrapper_from_label.opacity = 0.5
        
        self.navbar_wrapper_where_label = ft.Text()
        self.navbar_wrapper_where_label.value = "Where:"
        self.navbar_wrapper_where_label.size = 11
        self.navbar_wrapper_where_label.opacity = 0.5


        # Buttons
        self.add_account_btn = ft.OutlinedButton()
        self.add_account_btn.text = "Add account"
        self.add_account_btn.icon = ft.icons.ADD
        self.add_account_btn.expand = True
        self.add_account_btn.on_click = ...


        self.account_btn = ft.ElevatedButton()
        self.account_btn.text = "Sergey"
        self.account_btn.icon = ft.icons.ACCOUNT_CIRCLE
        self.account_btn.expand = True
        self.account_btn.on_click = ...

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
        self.navbar_wrapper_account_container = ft.Container()
        self.navbar_wrapper_account_container.width = 200
        self.navbar_wrapper_account_container.content = ft.Column([
            self.navbar_wrapper_from_label,
            self.navbar_wrapper_divider,
            self.account_btn,
            self.add_account_btn
        ])
        self.navbar_wrapper_account_container.content.width = 200


        self.navbar_wrapper_accounts_rows = ft.Row([
            self.navbar_wrapper_account_container
        ])

        # Containers:
        self.navbar_wrapper_accounts_side = ft.Container(ft.Column([
            self.navbar_wrapper_accounts_rows
        ]))
        self.navbar_wrapper_accounts_side.width = 200

        self.navbar_wrapper_settings = ft.Container(ft.Row([self.settings_btn]))
        self.navbar_wrapper_settings.width = 200
        self.navbar_wrapper_settings.height = 50


        # Main container
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

    def build(self):
        return self.navbar_wrapper


        

def application(page: ft.Page):
    page.add(
        ft.Row([Navbar()], expand=True)
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
