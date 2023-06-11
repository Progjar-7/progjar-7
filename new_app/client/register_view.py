import flet as ft
import database


def RegisterView(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "stretch"
    page.title = "Chat"
    page.scroll = "auto"

    def register(e):
        user = database.get_user(username=username_field.value)
        if user is not None:
            username_field.error_text = "User already exist"
            page.update()
        else:
            database.add_user(
                username=username_field.value, password=password_field.value
            )
            username_field.value = ""
            password_field.value = ""
            page.go("/login")
        print("username: ", username_field.value)
        print("password: ", password_field.value)

    def login(e):
        username_field.value = ""
        password_field.value = ""
        page.go("/login")

    username_field = ft.TextField(
        label="Username",
        autofocus=True,
        on_submit=register,
    )

    password_field = ft.TextField(
        label="Password",
        autofocus=True,
        on_submit=register,
    )

    page_layout = ft.Column(
        [
            ft.Text(f"Register", size=50),
            username_field,
            password_field,
            ft.Row(
                [
                    ft.ElevatedButton(text="Register", on_click=register),
                    ft.ElevatedButton(text="Back to Login", on_click=login),
                ],
                tight=True,
            ),
        ],
        tight=True,
    )

    return page_layout
