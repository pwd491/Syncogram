from sourcefiles.sqlite import SQLite
from functools import partial
import flet as ft


def navbar(page: ft.Page) -> ft.Container:

    def ui_generate_accounts(primary = False) -> ft.Row | ft.Container:
        sql = SQLite()
        accounts = sql.execute_accs(primary)
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

    def ui_add_account_dialog(e):
        sql = SQLite()
        accounts = sql.execute_all()
        if len(accounts) >= 2:
            return open_modal(e, dialog=ui_add_account_dialog_warning)
        return open_modal(e, dialog=ui_add_account_dialog_auth)

    def close_modal(e, dialog: ft.AlertDialog):
        dialog.open = False
        page.update()

    def open_modal(e, dialog: ft.AlertDialog):
        page.dialog = dialog
        dialog.open = True
        page.update()


    ui_add_account_dialog_warning = ft.AlertDialog(
        modal=True,
        title=ft.Text("Sorry 😔"),
        content=ft.Text(
            """The application does not support more than 1 account, expect in the future."""
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    ui_add_account_dialog_auth = ft.AlertDialog(
        modal=True,
        title=ft.Text("Authorization"),
        content=ft.Text(
            """asdasd."""
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    ui_add_account_dialog_auth.actions = [ft.TextButton("Okay", on_click=partial(close_modal, dialog=ui_add_account_dialog_auth))]
    ui_add_account_dialog_warning.actions = [ft.TextButton("Okay", on_click=partial(close_modal, dialog=ui_add_account_dialog_warning))]

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
                                                    bgcolor=ft.colors.with_opacity(
                                                        0.2,
                                                        ft.colors.ON_SECONDARY_CONTAINER,
                                                    ),
                                                ),
                                                ui_generate_accounts(True),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            text="Add account",
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
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text("Where:", size=11, opacity=0.5),
                                                ft.Container(
                                                    width=200,
                                                    height=0.5,
                                                    bgcolor=ft.colors.with_opacity(
                                                        0.2,
                                                        ft.colors.ON_SECONDARY_CONTAINER,
                                                    ),
                                                ),
                                                ui_generate_accounts(False),
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
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER),
    )
    return col
