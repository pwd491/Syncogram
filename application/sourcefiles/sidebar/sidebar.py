from flet import Row, IconButton, icons, MainAxisAlignment, TextField, TextAlign

txt_number = TextField(value="0", text_align=TextAlign.RIGHT, width=100)


def sidebar(page):
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    return Row(
        [
            IconButton(icons.REMOVE, on_click=minus_click),
            txt_number,
            IconButton(icons.ADD, on_click=plus_click),
        ],
        alignment=MainAxisAlignment.CENTER,
    )
