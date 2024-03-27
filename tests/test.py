import flet as ft

class Section1(ft.UserControl):
    def __init__(self, page: ft.Page):
        self.section = ft.Container()
        self.section.width = 250
        self.section.expand = True
        self.section.content = ft.Column()
        self.section.content.expand = True
        self.section.bgcolor = 'red'
        super().__init__()

    def build(self):
        return self.section

class Section2(ft.UserControl):
    def __init__(self, page: ft.Page):
        self.section = ft.Container()
        self.section.expand = True
        self.section.content = ft.Column()
        self.section.content.expand = True
        self.section.bgcolor = 'red'
        super().__init__()

    def build(self):
        return self.section
    

class Manager:
    def __init__(self, x,y):
        self.sec1 = x
        self.sec2 = y

    def build(self):
        return ft.Row([
            self.sec1,
            self.sec2
        ], expand=True)


def application(page: ft.Page) -> None:
    # page.add(
    #     ft.Row([
    #         Section1(page),
    #         Section2(page),
    #         ft.Container(ft.Column(expand=True), expand=True, bgcolor='red')
    #     ], expand=True)
    # )
    manager = Manager(Section1, Section2)
    

    # page.add(manager.build())

    page.update()


if __name__ == "__main__":
    ft.app(target=application)