import flet as ft
import time

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


def main(page: ft.Page):
  page.theme_mode = "light"
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll="auto"
  
  all_messages = ft.Column(scroll="auto", auto_scroll=True)
  
  def loop_chat_dummy():
    for index, message in enumerate(list_chat):
        all_messages.controls.append(
          # create user chat
            ft.Row([
                ft.Container(
                    padding=20,
                    border_radius=20,
                    bgcolor="blue200" if index % 2 == 0 else "green200",
                    content=ft.Column([
                        ft.Text(your_username.value, size=18, weight="bold") if index % 2 == 0 else ft.Text(
                            "Anyone", size=18, weight="bold"),
                        ft.Text(message, size=22)
                    ])
                )
            ], alignment="end" if index % 2 == 0 else "start")
        )

        page_layout.visible = True
        page.update()
        time.sleep(0.5)
  
  # Show all messages
  def get_message(e):
    if not your_username.value:
      your_username.error_text = "Please enter your name"
      page.update()
    elif not your_password.value:
      your_password.error_text = "Please enter your password"
      page.update()
    elif your_username.value != "messi" or your_password.value != "surabaya":
      your_username.error_text = "Your account is not registered"
      your_password.error_text = "Your account is not registered"
      page.update()
    else:
      page.dialog.open = False
      all_messages.controls.clear()
      loop_chat_dummy()
    
  # ========menambah list chat
  def send_message_click(e):
    if chat_field.value:
      all_messages.controls.append(ft.Text(chat_field.value))
      chat_field.value = ""
      page.update()
  
  # =============A dialog asking for a user display name
  your_username = ft.TextField(
    label="Enter your username",
    autofocus=True,
    on_submit=get_message,
  )
  
  your_password = ft.TextField(
    label="Enter your password",
    autofocus=True,
    on_submit=get_message,
  )
  
  page.dialog = ft.AlertDialog(
    open=True,
    modal=True,
    title=ft.Text("Welcome!"),
    content=ft.Column([your_username, your_password],tight=True),
    actions=[ft.ElevatedButton(text="Join chat", on_click=get_message)],
    actions_alignment="end",
    )# A dialog asking for a user display name

  # ================Chat messages field
  chat_field = ft.TextField(
        label="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )
  chat_cont = ft.Container(
    padding=20,
    border_radius=30,
    content=ft.Row([
      chat_field,
      ft.IconButton(icon="send",
      icon_size=30,
      on_click=send_message_click
      )
    ])
  )
  
  page_layout = ft.Column([
    ft.Container(
      height=500,
      padding=20,
      content=ft.Column([
        all_messages,
      ], scroll="auto", auto_scroll=True)
    ),
      chat_cont
  ])          
    
  # =========Add everything to the page
  page.add(page_layout)

ft.app(target=main)