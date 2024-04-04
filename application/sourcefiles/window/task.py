import flet as ft

class CustomTask(ft.UserControl):
    def __init__(self):
        super().__init__()
        
        self.progessbar = ft.ProgressBar()

        self.wrapper = ft.Column(
            [
                ft.Text("Doing"),
                ft.Column([
                    ft.Text("Doing something"),
                    self.progessbar
                ])
            ]
        )
        
        self.controls = self.wrapper

    def build(self):
        return self.wrapper