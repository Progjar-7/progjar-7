import flet as ft
import database
import json
from flet.security import encrypt, decrypt

SECRET_KEY = "PROGJAR"


def LoginView(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "stretch"
    page.title = "Chat"
    page.scroll = "auto"

    def login(e):
        user = database.get_user(username=username_field.value)
        if user is None:
            username_field.error_text = "User tidak dikenali"
            page.update()
        elif user["password"] != password_field.value:
            password_field.error_text = "Salah Password"
            page.update()
        else:
            page.client_storage.set("username", user["username"])
            page.client_storage.set("realm_name", user["realm_name"])

            json_user = json.dumps(user)
            token = encrypt(plain_text=json_user, secret_key=SECRET_KEY)
            page.client_storage.set("token", token)
            page_layout.open = False
            page_layout.update()
            page.go("/")

    def register(e):
        # page_layout.open = False
        username_field.value = ""
        password_field.value = ""
        page_layout.open = False
        page_layout.update()
        page.go("/register")

    username_field = ft.TextField(
        label="Username",
        autofocus=True,
        on_submit=login,
    )

    password_field = ft.TextField(
        label="Password",
        autofocus=True,
        on_submit=login,
    )

    page_layout = ft.Column(
        [
            ft.Text(f"Login", size=50),
            username_field,
            password_field,
            ft.Row(
                [
                    ft.ElevatedButton(text="Login", on_click=login),
                    ft.ElevatedButton(text="Register", on_click=register),
                ],
                tight=True,
            ),
        ],
        tight=True,
    )

    return page_layout
