import flet as ft

c1 = ft.Checkbox(
            label="Sync my favorite messages",
            value=True,
            disabled=True
        )
c2 = ft.Checkbox(
            label="Save the sequence of pinned messages",
            value=True,
            disabled=True
        )
c3 = ft.Checkbox(
            label="Sync my profile first name and second name.",
            value=False,
            disabled=False
        )

x: list[ft.Checkbox] = [c1, c2, c3].sort(key=lambda a: a.value is True)

print(x)