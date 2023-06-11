import flet as ft
import base64
from flet import icons

import json
import user
from client_private import ChatPrivateClient
from queue import Queue
import threading

User = user

# communication with server
chat_private = ChatPrivateClient()

messages = Queue()

current_username = ""

def listen(queue: Queue):
    try:
        while True:
          if not queue.empty():
              rcv = queue.get()
              result = json.loads(rcv)

              messages.put(result)

    except ConnectionResetError:
        print("Disconnected from the server.")
    except ConnectionAbortedError as e:
        print("Exit from group")
    except Exception as e:
        print(f"An error occurred in received_message: {e}")

# main page
def main(page: ft.Page):
  page.theme_mode = "light"
  page.horizontal_alignment = "stretch"
  page.title = "Chat"
  page.scroll="auto"
  
  all_messages = ft.Column(scroll="auto", auto_scroll=True)
  
  def loop_show_messages():
      while True:
          if not messages.empty():
              result = messages.get()
              print("dari loop show: ", result)

              match result['tipe_pesan']:
                 case 'PESAN_PRIVATE':
                    pengirim = result['data']['username_pengirim']

                    if pengirim == current_username:
                      all_messages.controls.append(
                        User.get_user_interface(username=pengirim, is_me=True, message=result['data']['pesan'])
                      )

                    else:
                       all_messages.controls.append(
                        User.get_user_interface(username=pengirim, is_me=False, message=result['data']['pesan'])
                      )

                    page_layout.visible = True
                    page.update()

                 case 'PESAN_FILE_PRIVATE':
                    pengirim = result['data']['username_pengirim']

                    if pengirim == current_username:
                      all_messages.controls.append(
                        User.get_file_interface(username=pengirim, is_me=True, filename=result['data']['filename'], content=result['data']['file_content'])
                      )

                    else:
                       all_messages.controls.append(
                        User.get_file_interface(username=pengirim, is_me=False, filename=result['data']['filename'], content=result['data']['file_content'])
                      )

                    page_layout.visible = True
                    page.update()
  
  
  # Show all messages
  def get_message(e):
    if not your_username.value:
      your_username.error_text = "Please enter your name"
      page.update()
    elif not your_username_destination.value:
      your_username_destination.error_text = "Please enter your partner"
      page.update()
    elif not your_password.value:
      your_password.error_text = "Please enter your password"
      page.update()
    # elif your_username.value != "messi" or your_password.value != "surabaya":
    #   your_username.error_text = "Your account is not registered"
    #   your_password.error_text = "Your account is not registered"
      # page.update()
    else:
      page.dialog.open = False
      all_messages.controls.clear()
      # connect to server client
      chat_private.start_chat()
      chat_private.send_message(f"OPENPRIVATE {your_username.value}")
      
      page.update()
      loop_show_messages()
    
  # ========menambah list chat
  def send_message_click(e):
    if chat_field.value:
      chat_private.send_message(f"SENDPRIVATE {your_username.value} {your_username_destination.value} {chat_field.value}")
      
      # global berarti mengakses variable current_username yang didefine di luar fungsi
      global current_username
      current_username = your_username.value
      
      chat_field.value = ""
      loop_show_messages()
      page.update()
  
  # ============= Bagian upload file
  def handle_file_upload(e: ft.FilePickerResultEvent):
    if (e.files) and len(e.files) > 0:
       filename = e.files[0].name

       with open(e.files[0].path, "rb") as f:
          content = base64.b64encode(f.read()).decode()
          chat_private.send_message(f"FILEPRIVATE {your_username.value} {your_username_destination.value} {filename} {content}")

  file_picker = ft.FilePicker(on_result=handle_file_upload)
  page.overlay.append(file_picker)

  # =============A dialog asking for a user display name
  your_username = ft.TextField(
    label="Enter your username",
    autofocus=True,
    on_submit=get_message,
  )
  
  your_username_destination = ft.TextField(
    label="Enter your partner username",
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
    content=ft.Column([your_username, your_username_destination, your_password],tight=True),
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
      ft.IconButton(icon=icons.UPLOAD_FILE, 
      icon_size=30,
      on_click=lambda _ : file_picker.pick_files(allow_multiple=False)
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
      chat_cont,
  ])          
    
  # =========Add everything to the page
  page.add(page_layout)

# Thread
receiver_thread = threading.Thread(target=listen, args=(chat_private.received_queue,))
receiver_thread.start()

ft.app(target=main)