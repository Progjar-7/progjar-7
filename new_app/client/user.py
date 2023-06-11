import flet as ft
import base64

list_chat = [
  "Halo",
  "Halo juga",
  "Apa kabar?",
  "Baik, kamu?",
  "Juga baik",
  "Halo",
  "Halo juga",
  "Apa kabar?",
  "Baik, kamu?",
  "Juga baik",
  "Halo",
  "Halo juga",
  "Apa kabar?",
  "Baik, kamu?",
  "Juga baik",
]

def get_user_interface(username, is_me=False, message=""):
  return ft.Row([
    ft.Container(
      padding=20,
      border_radius=20,
      bgcolor="blue200" if is_me else "green200",
      content=ft.Column([
        # ft.Text(username, size=18, weight="bold") if is_me else ft.Text(username, size=18, weight="bold"),
        ft.Text(username, size=18, weight="bold"),
        ft.Text(message, size=22)
      ])
    )
  ], alignment="end" if is_me else "start")

def save_file(filename, content):
  with open(filename, "wb") as f:
    bytes_content = base64.b64decode(content.encode())
    f.write(bytes_content)

def get_file_interface(username, filename, content, is_me=False):
  if is_me:
      return ft.Row([
        ft.Container(
          padding=20,
          border_radius=20,
          bgcolor="blue200",
          content=ft.Column([
            ft.Text(username, size=18, weight="bold"),
            ft.Text(f"file {filename} terkirim", size=22),
          ])
        )
      ], alignment="end")

  return ft.Row([
    ft.Container(
      padding=20,
      border_radius=20,
      bgcolor="green200",
      content=ft.Column([
        ft.Text(username, size=18, weight="bold"),
        ft.Text(filename, size=22),
        ft.TextButton(text=f"Download {filename}", on_click=save_file(filename, content))
      ])
    )
  ], alignment="start")