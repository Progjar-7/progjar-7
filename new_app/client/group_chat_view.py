import flet as ft
import threading
from room_chat import chat_group, listen, messages
import user

User = user

def GroupChatView(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "stretch"
    page.title = "Chat"
    page.scroll = "auto"

    all_messages = ft.Column(scroll="auto", auto_scroll=True)

    def loop_show_messages():
        while True:
            if not messages.empty():
                result = messages.get()
                print("dari loop show: ", result)

                match result["tipe_pesan"]:
                    case "PESAN_GROUP":
                        pengirim = result["data"]["username_pengirim"]

                    case "PESAN_FILE_GROUP":
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
                        page_layout.update()
                        page.update()

    def send_message_click(e):
        # pass
        all_messages.controls.clear()

        group_name = page.client_storage.get("join_group_name")
        username = page.client_storage.get("username")
        chat_group.send_message(f"SENDGROUP {group_name} {username} {chat_field.value}")

        page.update()
        loop_show_messages()    

    def get_message(e):
        pass

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
        ]
    )

    # =========Add everything to the page
    return page_layout

# Thread
receiver_thread = threading.Thread(target=listen, args=(chat_group.received_queue,))
receiver_thread.start()
