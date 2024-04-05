import flet as ft

class AboutApplication(ft.Container):
    def __init__(self):
        super().__init__()
        self.author = "Developed by Sergey Degtyar."
        self.license = "© GNU GENERAL PUBLIC LICENSE V2"
        self.text = ft.Text(f"If you found a bug, you can send feedback.\n{self.author}\n{self.license}")
        self.text.size = 9
        self.text.opacity = 0.5
        self.text.text_align = ft.TextAlign.CENTER

        self.wrapper = ft.Column([
            self.text
        ])
        self.wrapper.alignment = ft.MainAxisAlignment.CENTER
        self.content = self.wrapper
