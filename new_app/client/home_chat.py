import flet as ft

def HomeView(page):
  content = ft.Column(
    [
      ft.Row(
        [
          ft.Text(
            "Welcome to Our Simple Chat",
            size=50)
          ],
        alignment=ft.MainAxisAlignment.CENTER
        )
      ], alignment=ft.MainAxisAlignment.CENTER
    )
  
  return content
