from sourcefiles.utils import screensize
from sourcefiles import navbar
import flet as ft

SCREENWIDTH, SCREENHEIGHT = screensize()

def application(page: ft.Page):
    page.title = "Telegram Migrator"
    page.window_width = page.window_min_width = SCREENWIDTH * 0.5
    page.window_height = page.window_min_height = SCREENHEIGHT * 0.7
    page.window_top = SCREENHEIGHT / 8
    page.window_left = (SCREENWIDTH * 0.5) / 2


    container = ft.Container(
        content=ft.Container(
            ft.Container(
                ft.Card(
                    ft.Container(
                        ft.Column(
                            [
                                ft.Row(
                                    [ft.Text("From:", size=11, opacity=0.45)]
                                ),
                                ft.Divider(height=1, opacity=0.45),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Sergey", icon=ft.icons.ACCOUNT_BOX, expand=True, bgcolor=ft.colors.SECONDARY_CONTAINER, color=""),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Add account", icon="add", expand=True),
                                    ]
                                ),
                                ft.Row(
                                    [ft.Text("Where:", size=11, opacity=0.45)]
                                ),
                                ft.Divider(height=1, opacity=0.45),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Anton", icon=ft.icons.ACCOUNT_BOX, expand=True, bgcolor=ft.colors.SECONDARY_CONTAINER, color=""),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Add account", icon="add", expand=True),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Settings", icon="settings", expand=True),
                                    ],
                                ),

                            ],
                        ), padding=20
                    )
                ),
        ),
        expand=True,
        width=250,

    )
    )

    
    page.add(
        ft.Row(
            [
                container,
            ], expand=True, 
        )
    )


    page.update()


if __name__ == "__main__":
    ft.app(target=application)
