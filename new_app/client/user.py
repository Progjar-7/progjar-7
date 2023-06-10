import flet as ft

def get_user_interface(username, is_me=True, message=""):
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
