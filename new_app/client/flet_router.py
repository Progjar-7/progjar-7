import flet as ft

# views
from home_chat import HomeView
from room_chat import PrivateView
from join_group_chat import JoinGroupView

class Router:
  def __init__(self, page):
    self.page = page
    self.ft = ft
    self.routes = {
      "/": HomeView(page),
      "/private": PrivateView(page),
      "/add-group": JoinGroupView(page)
      # "/group": SettingsView(page)
      }
    self.body = ft.Container(content=self.routes['/'])
    
  def route_change(self, route):
    self.body.content = self.routes[route.route]
    self.body.update()
