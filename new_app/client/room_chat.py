import flet as ft

def main(page: ft.Page):
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll="auto"
  
  all_messages = ft.Column(scroll="auto")
    
    # menambah list chat
  def send_message_click(e):
    if chat_field.value:
      all_messages.controls.append(ft.Text(chat_field.value))
      chat_field.value = ""
      page.update()
  
  # Chat messages field
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
      content=ft.Column([
        all_messages,
      ], scroll="auto")
    ),
      chat_cont
  ])          
    
    # Add everything to the page
  
  page.add(page_layout)

ft.app(target=main)