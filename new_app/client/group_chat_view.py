import flet as ft

def GroupChatView(page: ft.Page):
  page.theme_mode = "light"
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll = "auto"

  all_messages = ft.Column(scroll="auto", auto_scroll=True)

  def send_message_click(e):
    pass

  def get_message(e):
    group_dialog.open = False
    group_dialog.update()
    pass

  group_name = ft.TextField(
      label="Enter your group name",
      autofocus=True,
      on_submit=get_message,
  )

  group_dialog = ft.AlertDialog(
      open=True,
      modal=True,
      title=ft.Text("Enter group name"),
      content=ft.Column(
          [group_name], tight=True),
      actions=[ft.ElevatedButton(text="Join chat", on_click=get_message)],
      actions_alignment="end",
  )

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
                      ),
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
      chat_cont,
      group_dialog
  ])

  # =========Add everything to the page
  return page_layout
