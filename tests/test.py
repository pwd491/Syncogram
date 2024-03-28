from functools import partial
import flet as ft

class MainContainer(ft.Container):
    def __init__(self):
        super().__init__(
            content = ft.Column(),
            expand=True,
            bgcolor='yellow'
        )

class AuthorizationModalWindow(ft.AlertDialog):
    def __init__(self):
        super().__init__(
            True, ft.Text("Test")
        )


class UserBar(ft.Container):
    def __init__(self, page: ft.Page):
        self.page: ft.Page = page

        self.button = ft.OutlinedButton()
        self.button.text = "Button"
        self.button.on_click = self.click
        

        self.alert = ft.AlertDialog()
        self.alert.modal = True
        self.alert.title = ft.Text("Test Alert Dialog")
        self.alert_close = ft.TextButton("Close", on_click=self.close)
        self.alert.actions.append(self.alert_close)
        self.alert.bgcolor = 'yellow'
        
        super().__init__(
            content = ft.Column([self.button],width=250,expand=True),
            bgcolor='red',
        )

    def click(self, e):
        self.page.dialog = self.alert
        self.alert.open = True
        self.page.update()

    def close(self, e):
        self.page.dialog = self.alert
        self.alert.open = False
        self.page.update()
 

def main(page: ft.Page):
    window = ft.Row()
    window.expand = True
    window.controls.append(UserBar(page))

    page.add(window)
    page.update()

ft.app(target=main)