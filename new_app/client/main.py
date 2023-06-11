import flet as ft

from flet_router import Router
from navbar import Navbar


def main(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "stretch"
    page.title = "Chat"
    page.scroll = "auto"
    page.appbar = Navbar(page)
    myRouter = Router(page)
    page.on_route_change = myRouter.route_change

    page.add(myRouter.body)
    page.go("/login")


ft.app(target=main)
