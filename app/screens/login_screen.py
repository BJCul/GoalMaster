# screens/login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string(
    """
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDTextField:
            id: username_input
            hint_text: "Enter username"
            required: True
            helper_text: "Required field"
            helper_text_mode: "on_focus"

        MDTextField:
            id: password_input
            hint_text: "Enter password"
            password: True
            required: True
            helper_text: "Required field"
            helper_text_mode: "on_focus"

        MDRaisedButton:
            text: "Login"
            on_press: root.login_user(username_input.text, password_input.text)

        MDRaisedButton:
            text: "Register"
            on_press: root.manager.current = 'register_screen'
    """
)


class LoginScreen(Screen):
    def login_user(self, username, password):
        # Implement your login logic here
        if self.validate_credentials(username, password):
            print(f"Login successful. Welcome, {username}!")
            # Navigate to the main goal screen after login
            self.manager.current = 'goal_screen'
        else:
            print("Login failed. Please check your credentials.")

    def validate_credentials(self, username, password):
        # Replace this with your actual authentication logic (e.g., checking against a database)
        # For simplicity, this example allows any non-empty username and password
        return bool(username) and bool(password)
