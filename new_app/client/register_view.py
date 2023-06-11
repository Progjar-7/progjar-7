import flet as ft


def RegisterView(page: ft.Page):
  page.theme_mode = "light"
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll = "auto"
  
  def register(e):
    print("username: ", username_field.value)
    print("realm: ", realm_field.value)
    print("password: ", password_field.value)
    page.go("/login")

  def login(e):
    username_field.value = ""
    password_field.value = ""
    page.go("/login")

  username_field = ft.TextField(
      label="Username",
      autofocus=True,
      on_submit=register,
  )
  
  realm_field = ft.TextField(
      label="Realm name",
      autofocus=True,
      on_submit=register,
  )

  password_field = ft.TextField(
      label="Password",
      autofocus=True,
      on_submit=register,
  )

  page_layout = ft.Column([
      ft.Text(
          f"Register",
          size=50),
    username_field,
    realm_field,
    password_field,
    ft.Row([
        ft.ElevatedButton(text="Register", on_click=register),
        ft.ElevatedButton(text="Back to Login", on_click=login),
    ], tight=True)
  ], tight=True)
  
  return page_layout
