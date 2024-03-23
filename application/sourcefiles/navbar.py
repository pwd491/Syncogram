import flet as ft


def navbar(page: ft.Page) -> ft.Container:

    def close_modal(e):
        ui_add_account_dialog.open = False
        page.update()

    def open_modal(e):
        page.dialog = ui_add_account_dialog
        ui_add_account_dialog.open = True
        page.update()



    ui_add_account_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Sorry 😔"),
        content=ft.Text("""The application does not support more than 1 account, expect in the future."""),
        actions=[
            ft.TextButton("Okay", on_click=close_modal),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )



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
                                                    bgcolor=ft.colors.with_opacity(0.2, ft.colors.ON_SECONDARY_CONTAINER),
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            "Sergey",
                                                            icon=ft.icons.ACCOUNT_BOX,
                                                            expand=True,
                                                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                                                        )
                                                    ]
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            text="Add account",
                                                            icon="add",
                                                            expand=True,
                                                            on_click=open_modal
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
                                                    bgcolor=ft.colors.with_opacity(0.2, ft.colors.ON_SECONDARY_CONTAINER),
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            "Anton",
                                                            icon=ft.icons.ACCOUNT_BOX,
                                                            expand=True,
                                                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                                                        )
                                                    ]
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton(
                                                            "Add account",
                                                            icon="add",
                                                            expand=True,
                                                            on_click=open_modal
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
