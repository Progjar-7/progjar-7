import flet as ft

def HomeView(page):
  content = ft.Column(
    [
      ft.ResponsiveRow(
        [
          ft.Text(
            f"Welcome to Our Simple Chat!",
            size=50)
          ],
        alignment=ft.MainAxisAlignment.CENTER
        )
      ], alignment=ft.MainAxisAlignment.CENTER
    )
  
  return content
