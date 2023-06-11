import flet as ft

def LoginView(page: ft.Page):
  page.theme_mode = "light"
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll="auto"
  
  def login(e):
    print("username: ", username_field.value)
    print("password: ", password_field.value)
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
  
  page_layout = ft.Column([
      ft.Text(
          f"Login",
          size=50),
      username_field,
      password_field,
      ft.Row([
          ft.ElevatedButton(text="Login", on_click=login),
          ft.ElevatedButton(text="Register", on_click=register),
      ], tight=True)
  ], tight=True)
  
  return page_layout