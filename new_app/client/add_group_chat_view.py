import flet as ft
import json
import user
from client_group import ChatGroupClient
from queue import Queue
import threading

# communication with server
chat_group = ChatGroupClient()

messages = Queue()


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


def AddGroupView(page):
  
  def loop_show_messages():
    while True:
      if not messages.empty():
        result = messages.get()
        print("dari loop show: ", result)

  def get_group_name(e):
    if not group_name_field.value:
      group_name_field.error = "Group name cannot be empty"
      page.update()
    else:
      print("group name chat: ", group_name_field.value)
      page.client_storage.set("new_group_name", group_name_field.value)  # keyy
      
      chat_group.send_message(f"CREATE {group_name_field.value}")
      
      page_layout.open = False
      page_layout.update()
      loop_show_messages()
      page_layout.update()
      
      # page.go("/")

  group_name_field = ft.TextField(
      label="Group Name",
      autofocus=True,
      on_submit=get_group_name,
  )

  page_layout = ft.AlertDialog(
      title=ft.Text("Add Group Chat"),
      open=True,
      modal=True,
      content=group_name_field,
      actions=[ft.ElevatedButton(text=ft.icons.ADD, on_click=get_group_name)],
  )

  return page_layout


# Thread
receiver_thread = threading.Thread(
    target=listen, args=(chat_group.received_queue,))
receiver_thread.start()
