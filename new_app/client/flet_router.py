import flet as ft

# views
from home_chat import HomeView
from room_chat import PrivateView
from join_group_chat import JoinGroupView
from login_view import LoginView
from register_view import RegisterView

class Router:
  def __init__(self, page):
    self.page = page
    self.ft = ft
    self.routes = {
      "/": HomeView(page),
      "/login": LoginView(page),
      "/register": RegisterView(page),
      "/private": PrivateView(page),
      "/add-group": JoinGroupView(page)
      # "/group": SettingsView(page)
      }
    self.body = ft.Container(content=self.routes['/'])
    
  def route_change(self, route):
    self.body.content = self.routes[route.route]
    self.body.update()
