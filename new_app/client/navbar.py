import flet as ft


def Navbar(page):
  Navbar = ft.AppBar(
    leading=ft.Icon(ft.icons.TAG_FACES_ROUNDED),
    leading_width=40,
    title=ft.Text("Simple Chat"),
    center_title=False,
    bgcolor=ft.colors.SURFACE_VARIANT,
    actions=[
      ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/')),
      ft.IconButton(ft.icons.PERSON_ROUNDED, on_click=lambda _: page.go('/private')),
      ft.IconButton(ft.icons.GROUP_ADD_ROUNDED, on_click=lambda _: page.go('/add-group'))
      # ft.IconButton(ft.icons.GROUP_ADD_ROUNDED, on_click=lambda _: page.go('/group'))
      ]
    )

  return Navbar