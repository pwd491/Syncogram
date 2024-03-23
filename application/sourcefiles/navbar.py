import flet as ft

def navbar(page: ft.Page) -> ft.Container:
    col = ft.Container(
           ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                
                                ft.Row(
                                    [
                                        ft.Container(
                                            ft.Column([
                                                ft.Text("From:", size=11, opacity=0.5),
                                                ft.Container(width=200, height=0.5, bgcolor="white", opacity=0.1),
                                                ft.Row([ft.ElevatedButton("Sergey", icon=ft.icons.ACCOUNT_BOX, expand=True, bgcolor=ft.colors.SECONDARY_CONTAINER)]),
                                                ft.Row([ft.ElevatedButton("Add account", icon="add", expand=True),])
                                            ],
                                            alignment=ft.MainAxisAlignment.START
                                            ),
                                            width=200,
                                        ),
                                    ]
                                ),

                                ft.Row(
                                    [
                                        ft.Container(
                                            ft.Column([
                                                ft.Text("Where:", size=11, opacity=0.5),
                                                ft.Container(width=200, height=0.5, bgcolor="white", opacity=0.1),
                                                ft.Row([ft.ElevatedButton("Anton", icon=ft.icons.ACCOUNT_BOX, expand=True, bgcolor=ft.colors.SECONDARY_CONTAINER)]),
                                                ft.Row([ft.ElevatedButton("Add account", icon="add", expand=True),])
                                            ], alignment=ft.MainAxisAlignment.START
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
                               ft.ElevatedButton("Settings", icon=ft.icons.SETTINGS, expand=True, height=45) 
                            ],
                        ),
                        width=200,
                        height=50,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
           ),
           width=250,
           padding=20,
           border_radius=ft.BorderRadius(10,10,10,10),
           bgcolor=ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER),
    )
    return col


