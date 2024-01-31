from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder

kv = """
Screen:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            text: "GoalMaster: Aim High"
            font_style: 'H4'
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: username
            hint_text: "User ID"
            size_hint_x: None
            width: 300
            pos_hint: {'center_x': 0.5}
        
        MDTextField:
            id: password
            hint_text: "Password"
            size_hint_x: None
            width: 300
            password: True
            pos_hint: {'center_x': 0.5}

        MDRoundFlatButton:
            text: "Forgot User ID or Password"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            pos_hint: {'center_x': 0.5}

        MDRoundFlatButton:
            text: "Don't have an account yet? Sign up now!"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            pos_hint: {'center_x': 0.5}
"""

class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_string(kv)
        return screen

DemoApp().run()