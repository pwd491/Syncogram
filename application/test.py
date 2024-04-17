import flet as ft
import gettext

path = gettext.find('base', 'application/locales')

translations = gettext.translation('base', 'application/locales', fallback=True)
_ = translations.gettext

async def main(page: ft.Page):
    page.title = _("Hello world")
    page.update()

ft.app(main)