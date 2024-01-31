# screens/startup_screen.py
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from login_screen import LoginScreen

startupscreen = """
<StartupScreen>
    name: 'StartupScreen'
    canvas.before:
        Color:
            rgba: (0,0,0,1)
        Rectangle:
            size: self.size
            pos: self.pos
    Image
        id: img_logo
        allow_strech: True
        keep_ratio: False
        source: './data/images/icon.png'
        size_hint_y: .5
        size_hint_x: .8
        pos_hint : {'center_x': .5, 'center_y': .5}
        
"""


class StartupScreen(Screen):
    Builder.load_string(startupscreen)

    def __init__(self):
        super(StartupScreen, self).__init__()

    def on_enter(self, *args):
        from kivy.clock import Clock

        Clock.schedule_once(lambda dt: self.load_navigation(), 2)

    @staticmethod
    def load_navigation():

        app = App.get_running_app()
        app.theme_cls = ThemeManager()
        app.theme_cls.primary_palette = "Teal"
        app.theme_cls.accent_palette = "Amber"
        app.theme_cls.theme_style = "Light"
        app.theme_cls.theme_style = app.config.get("CustSettings", "mode")

        from screens import Screens

        app.screens = Screens()
        app.screens.app = app

        app.screens.primary_widget = LoginScreen()
        app.root.add_widget(app.screens.primary_widget)
        app.root.current = "LoginScreen"