import flet as ft
from room_chat import chat_group

def JoinGroupView(page):
    def get_group_name(e):
        print("group name: ", group_name_field.value)
        page.client_storage.set("join_group_name", group_name_field.value)  # keyy
        page_layout.open = False
        page_layout.modal = False
        page_layout.update()
        page.update()
        page.go("/group")

    group_name_field = ft.TextField(
        label="Group Name",
        autofocus=True,
        on_submit=get_group_name,
    )
    group_host_field = ft.TextField(
        label="Host",
        autofocus=True,
        on_submit=get_group_name,
    )
    group_port_field = ft.TextField(
        label="port",
        autofocus=True,
        on_submit=get_group_name,
    )

    page_layout = ft.AlertDialog(
        title=ft.Text("Join Group Chat"),
        open=True,
        modal=True,
        content=ft.Column([group_name_field, group_host_field, group_port_field], tight=True),
        actions=[ft.ElevatedButton(text=ft.icons.ADD, on_click=get_group_name)],
    )

    return page_layout
