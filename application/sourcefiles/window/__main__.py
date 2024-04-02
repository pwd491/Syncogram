import flet as ft

class MainWindow(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page

        self.sticker = ft.Image()
        self.sticker.src = "/Users/admin/Development/Syncogram/application/assets/sticker2.gif"
        self.sticker.width = 200

        self.sticker_text = ft.Text("To get started, log in to at least 2 accounts")

        self.wrapper =  ft.Column([self.sticker, self.sticker_text])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.wrapper.horizontal_alignment = ft.CrossAxisAlignment.CENTER


        self.content = self.wrapper
        self.expand = True
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.SECONDARY_CONTAINER)
        self.border_radius = ft.BorderRadius(10, 10, 10, 10)
        self.padding = 20