import flet as ft
import base64
from flet import icons
from flet.security import encrypt, decrypt

import json
import user
from client_private import ChatPrivateClient
from queue import Queue
import threading

import database

User = user

# communication with server
chat_private = ChatPrivateClient()

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


# main page
def PrivateView(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "stretch"
    page.title = "Chat"
    page.scroll = "auto"

    all_messages = ft.Column(scroll="auto", auto_scroll=True)

    # SECRET_KEY = "PROGJAR"
    # Show all messages
    def loop_show_messages():
        while True:
            if not messages.empty():
                result = messages.get()
                print("dari loop show: ", result)

                match result["tipe_pesan"]:
                    case "PESAN_PRIVATE":
                        pengirim = result["data"]["username_pengirim"]

                        if pengirim == page.client_storage.get("username"):
                            all_messages.controls.append(
                                User.get_user_interface(
                                    username=pengirim,
                                    is_me=True,
                                    message=result["data"]["pesan"],
                                )
                            )

                        else:
                            all_messages.controls.append(
                                User.get_user_interface(
                                    username=pengirim,
                                    is_me=False,
                                    message=result["data"]["pesan"],
                                )
                            )

                        page_layout.visible = True
                        page.update()

                    case "PESAN_FILE_PRIVATE":
                        pengirim = result["data"]["username_pengirim"]

                        if pengirim == page.client_storage.get("username"):
                            all_messages.controls.append(
                                User.get_file_interface(
                                    username=pengirim,
                                    is_me=True,
                                    filename=result["data"]["filename"],
                                    content=result["data"]["file_content"],
                                )
                            )

                        else:
                            all_messages.controls.append(
                                User.get_file_interface(
                                    username=pengirim,
                                    is_me=False,
                                    filename=result["data"]["filename"],
                                    content=result["data"]["file_content"],
                                )
                            )

                        page_layout.visible = True
                        page.update()

    def get_message(e):
        print ("isSameGroup: ", isSameGroup.value)
        if not your_username_destination.value:
            your_username_destination.error_text = "Please enter your partner"
            page.update()
        else:
            auth_dialog.open = False
            all_messages.controls.clear()
            page.client_storage.set("destination", your_username_destination.value)
            # connect to server client
            chat_private.start_chat()

            current_username = page.client_storage.get("username")
            chat_private.send_message(f"OPENPRIVATE {current_username}")

            page.update()
            loop_show_messages()

    # ========menambah list chat
    def send_message_click(e):
        if chat_field.value:
            username = page.client_storage.get("username")
            chat_private.send_message(
                f"SENDPRIVATE {username} {your_username_destination.value} {chat_field.value}"
            )

            chat_field.value = ""
            loop_show_messages()
            page.update()

    # ============= Bagian upload file
    def handle_file_upload(e: ft.FilePickerResultEvent):
        if (e.files) and len(e.files) > 0:
            filename = e.files[0].name
            username = page.client_storage.get("username")
            destination = page.client_storage.get("destination")

            with open(e.files[0].path, "rb") as f:
                content = base64.b64encode(f.read()).decode()
                chat_private.send_message(
                    f"FILEPRIVATE {username} {destination} {filename} {content}"
                )

    file_picker = ft.FilePicker(on_result=handle_file_upload)
    page.overlay.append(file_picker)

    # =============A dialog 
    isSameGroup = ft.Checkbox(label="Saya dari kelompok 7", value=False)
    your_username_destination = ft.TextField(
        label="Enter your partner username",
        autofocus=True,
        on_submit=get_message,
    )
    your_host = ft.TextField(
        label="Enter Host IP (optional)",
        autofocus=True,
        on_submit=get_message,
    )
    your_port = ft.TextField(
        label="Enter Port (optional)",
        autofocus=True,
        on_submit=get_message,
    )

    auth_dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([your_username_destination, your_host, your_port, isSameGroup], tight=True),
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
        content=ft.Row(
            [
                chat_field,
                ft.IconButton(icon="send", icon_size=30, on_click=send_message_click),
                ft.IconButton(
                    icon=icons.UPLOAD_FILE,
                    icon_size=30,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                ),
            ]
        ),
    )

    page_layout = ft.Column(
        [
            ft.Container(
                height=500,
                padding=20,
                content=ft.Column(
                    [
                        all_messages,
                    ],
                    scroll="auto",
                    auto_scroll=True,
                ),
            ),
            chat_cont,
            auth_dialog,
        ]
    )

    # =========Add everything to the page
    return page_layout


# Thread
receiver_thread = threading.Thread(target=listen, args=(chat_private.received_queue,))
receiver_thread.start()

# ft.app(target=main)
