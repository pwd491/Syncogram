from functools import partial
from typing import Any
from sql import SQLite
import flet as ft



class Navbar(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        self.database = SQLite()
        self.page: ft.Page = page

        
        # Labels
        ### Нужно переделать !!!
        self.navbar_wrapper_from_label = ft.Text()
        self.navbar_wrapper_from_label.value = "From:"
        self.navbar_wrapper_from_label.size = 11
        self.navbar_wrapper_from_label.opacity = 0.5
        
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


        # Modals
        self.window_authentication = ft.AlertDialog()
        self.window_authentication.modal = True
        self.window_authentication.title = "Authorization"
        self.window_authentication.content = [ft.Text('asdads')],
        self.window_authentication.actions_alignment = ft.MainAxisAlignment.END
        self.window_authentication.actions = [
            ft.TextButton("Yes", on_click=...),
            ft.TextButton("No", on_click=...),
        ]
        self.window_authentication.open = True


        # Divider
        self.navbar_wrapper_divider = ft.Container()
        self.navbar_wrapper_divider.width = 200
        self.navbar_wrapper_divider.height = 0.5
        self.navbar_wrapper_divider.bgcolor = ft.colors.ON_SECONDARY_CONTAINER


        # Containers
        ### [Major block to display accounts on navbar]
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
        super().__init__()



    def ui_account_button(self, account_id, account_name) -> ft.ElevatedButton:
        """
        User card and Button. On click suggesting to logout from session.
        """
        button = ft.ElevatedButton()
        button.text = account_name
        button.icon = ft.icons.ACCOUNT_CIRCLE
        button.expand = True
        button.key = account_id
        button.on_click = ...
        return button


    def ui_add_account_button(self, status) -> ft.OutlinedButton:
        """
        User authorization button. On click opening modal window to authenticate.

        Arguments:
            status: defines status of account (can be <primary> or <secondary>) 
        """
        button = ft.OutlinedButton()
        button.text = "Add account"
        button.icon = ft.icons.ADD
        button.expand = True
        button.key = status
        button.on_click = partial(self.ui_add_account_process, status=button.key)
        return button


    def ui_add_account_process(self, e, status):
        """
        Processing authorizations via Telegram. Opens modal window to auth via
        QR code or by telephone number. First of all checks count sessions in
        Database. By defaults doesn't access to add account if accounts >= 2. 
        QR code authenticate is primary.

        Arguments:
            e: event by flet.
            status: defines status of account (can be <primary> or <secondary>)
        """
        # accounts: list[Any] = self.database.get_accounts()
        
        self.page.add(ft.Row([ft.Text('asd')]))
        # self.page.dialog.open = True

        # self.update()

        # if len(accounts) >= 2:
        #     return print("cancel")


    def ui_generate_account_container(self, status) -> ft.Column:
        """
        Generates account container using list of users from Database. If
        counts of accounts = 0, returns column with empty container and
        button <add account>.

        Arguments:
            status: defines account priority (can be <primary> & <secondary>). 
        """
        accounts: list[Any] = self.database.get_accounts()

        navbar_wrapper_account_container = ft.Column()
        navbar_wrapper_account_container.key = status
        navbar_wrapper_account_container.width = 200
        navbar_wrapper_account_container.controls = []


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
    

class Section(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.section = ft.Container()
        self.section.content = ft.Column([ft.Text('asd')])
        self.section.bgcolor = ft.colors.SECONDARY_CONTAINER
        self.section.expand = True
        self.section.content.expand = True
        self.section.border_radius = ft.BorderRadius(10, 10, 10, 10)
        super().__init__()

    def build(self) -> ft.Container:
        return self.section

def application(page: ft.Page) -> None:
    page.add(
        ft.Row([
            Navbar(page),
            Section(page),
            # ft.Container(ft.Column(expand=True), expand=True, bgcolor='red')
        ], expand=True)
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=application)
