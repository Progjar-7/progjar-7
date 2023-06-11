import flet as ft


def HomeView(page):
    # Define button menu
    menu = ft.Row(
        [
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.LOGIN,
                        on_click=lambda _: page.go("/login"),
                        icon_size=50,
                    ),
                    ft.Text("Logout", size=20),
                ]
            ),
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.HOME, on_click=lambda _: page.go("/"), icon_size=50
                    ),
                    ft.Text("Home", size=20),
                ]
            ),
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.PERSON_ROUNDED,
                        on_click=lambda _: page.go("/private"),
                        icon_size=50,
                    ),
                    ft.Text("Private", size=20),
                ]
            ),
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.ADD_BOX_ROUNDED,
                        on_click=lambda _: page.go("/join-group"),
                        icon_size=50,
                    ),
                    ft.Text("Join Group", size=20),
                ]
            ),
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.GROUP_ADD_ROUNDED,
                        on_click=lambda _: page.go("/add-group"),
                        icon_size=50,
                    ),
                    ft.Text("Add Group", size=20),
                ]
            ),
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.GROUP,
                        on_click=lambda _: page.go("/group"),
                        icon_size=50,
                    ),
                    ft.Text("Group", size=20),
                ],
            ),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    # Create the home page layout

    return menu
