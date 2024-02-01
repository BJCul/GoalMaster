from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty



class TrackerScreen(MDBoxLayout):
    pass

class DashboardScreen(MDBoxLayout):
    theme_text_color = "Custom"
    screen_mngr = ObjectProperty(None)

    def piggycard_click(self):
        print("ehehehehe")

    def otherscrn(self):
        TrackerScreen()


class dashboard(MDApp):
    def build(self):
        return Builder.load_file("dashboard.kv")
    


if __name__ == '__main__':
    Window.size = (360, 636)
    Window.top = 30
    Window.left = 900
    dashboard().run()