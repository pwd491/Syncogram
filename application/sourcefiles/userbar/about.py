import flet as ft

class AboutApplication(ft.Container):
    def __init__(self):
        super().__init__()
        self.author = "Developed by Sergey Degtyar."
        self.license = "© GNU GENERAL PUBLIC LICENSE V2"


        self.text = ft.Text(f"If you found a bug, you can send feedback.\n{self.author}\n{self.license}")
        self.text.size = 10
        self.text.opacity = 0.5
        self.text.text_align = ft.TextAlign.CENTER

        self.wrapper = ft.Column([
            # ft.TextButton('GitHub source', url="https://github.com/pwd491/syncogram.git"),
            self.text
        ])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER


        self.content = self.wrapper
        # self.bgcolor = "red"
        # self.expand = True