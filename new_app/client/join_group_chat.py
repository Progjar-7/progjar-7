import flet as ft

def JoinGroupView(page):
  
  def get_group_name(e):
    print("group name: ", group_name_field.value)
    page.client_storage.set("join_group_name", group_name_field.value) #keyy
    page_layout.open = False
    page_layout.update()
    page.go("/")
  
  group_name_field = ft.TextField(
    label="Group Name",
    autofocus=True,
    on_submit=get_group_name,
  )
  
  page_layout = ft.AlertDialog(
    title=ft.Text("Join Group Chat"),
    open=True,
    modal=True,
    content=group_name_field,
    actions=[ft.ElevatedButton(text=ft.icons.ADD, on_click=get_group_name)],
  )
  
  return page_layout
