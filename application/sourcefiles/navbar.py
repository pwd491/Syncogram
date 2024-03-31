from sourcefiles.sqlite import SQLite
from tests.utils import clr_on_secondary_container
from tests.utils import clr_secondary_container
from functools import partial
import flet as ft


class NavBar():
    def __init__(self, page,):
        super().__init__()
        self.page: ft.Page = page
        # self.


    def _update(self):
        self.page.add()

    



def navbar(page: ft.Page) -> ft.Container:

    def ui_generate_accounts(prime = False) -> ft.Row | ft.Container:
        sql = SQLite()
        accounts = sql.execute_accs(prime)
        if len(accounts) != 0:
            return ft.Row(
                    [
                    ft.ElevatedButton(
                        accounts[0][1],
                        icon=ft.icons.ACCOUNT_BOX,
                        expand=True,
                        bgcolor=ft.colors.SECONDARY_CONTAINER,
                        )
                    ]
                    )
        return ft.Container()
    
    def ui_authorization_account(e, prime = False):
        sql = SQLite()
        result = sql.add_account(ui_id_field.value, ui_name_field.value, *prime)
        print(result)
        close_modal(e, ui_add_account_dialog_auth)

    def close_modal(e, dialog: ft.AlertDialog):
        dialog.open = False
        page.update()

    def open_modal(e, dialog: ft.AlertDialog, *prime):
        page.dialog = dialog
        print(dialog.data)
        if dialog.data == "auth":
            dialog.actions = [ft.TextButton("Log In", on_click=partial(ui_authorization_account, prime=prime))]
        else:
            dialog.actions = [ft.TextButton("Okay", on_click=partial(close_modal, dialog=ui_add_account_dialog_warning))]
        dialog.open = True
        page.update()


    ui_add_account_dialog_warning = ft.AlertDialog(
        modal=True,
        title=ft.Text("Sorry 😔"),
        content=ft.Text(
            """The application does not support more than 1 account, expect in the future."""
        ),
        actions_alignment=ft.MainAxisAlignment.END,
        data="warn"
    )

    ui_id_field = ft.TextField(label="Telegram ID", keyboard_type=ft.KeyboardType.NUMBER)
    ui_name_field = ft.TextField(label="First name")

    ui_add_account_dialog_auth = ft.AlertDialog(
        modal=False,
        title=ft.Text("Authorization"),
        content=ft.ResponsiveRow([ui_id_field, ui_name_field]),
        actions_alignment=ft.MainAxisAlignment.END,
        data="auth"
    )

    def ui_add_account_dialog(e, prime = False):
        sql = SQLite()
        accounts = sql.execute_all()
        if len(accounts) >= 2:
            return open_modal(e, dialog=ui_add_account_dialog_warning)
        return open_modal(e, ui_add_account_dialog_auth, prime)

    col = ft.Container(
        ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text("From:", size=11, opacity=0.5),
                                                ft.Container(
                                                    width=200,
                                                    height=0.5,
                                                    bgcolor=clr_on_secondary_container(page.platform_brightness.value, page.theme_mode.value),
                                                ),
                                                ui_generate_accounts(True),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            text="Add account",
                                                            icon="add",
                                                            expand=True,
                                                            on_click=partial(ui_add_account_dialog, prime=True),
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        width=200,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text("Where:", size=11, opacity=0.5),
                                                ft.Container(
                                                    width=200,
                                                    height=0.5,
                                                    bgcolor=clr_on_secondary_container(page.platform_brightness.value, page.theme_mode.value),
                                                ),
                                                ui_generate_accounts(),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            "Add account",
                                                            icon="add",
                                                            expand=True,
                                                            on_click=ui_add_account_dialog,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        width=200,
                                    ),
                                ]
                            ),
                        ]
                    ),
                    width=200,
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Settings",
                                icon=ft.icons.SETTINGS,
                                expand=True,
                                height=45,
                            )
                        ],
                    ),
                    width=200,
                    height=50,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        width=250,
        padding=20,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        bgcolor=clr_secondary_container(page.platform_brightness.value, page.theme_mode.value),
    )
    return col
