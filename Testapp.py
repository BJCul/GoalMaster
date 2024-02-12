from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import os


Window.size = (360, 640)

# class BaseScreen(MDScreen):
#     def __init__(self, *args, **kwargs):
#         # print(MDApp.get_running_app())
#         super().__init__(*args, **kwargs)
    
class ContentNavigationDrawer(BoxLayout):
        pass



# screen_manager = MDScreenManager()
# Adding screens to the screen manager
# screen_manager.add_widget(SampleScreen())
# screen_manager.add_widget(StartupScreen(name='startup'))
# screen_manager.add_widget(Startup1Screen(name='startup1'))
# screen_manager.add_widget(Startup2Screen(name='startup2'))
# screen_manager.add_widget(LoginScreen(name='login'))
# screen_manager.add_widget(LoginScreen(name='signup'))
# screen_manager.add_widget(DashboardScreen(name='dashboard'))


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("Testapp.kv")

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Steelblue"

        screen_manager = MDScreenManager()
        screen_manager.add_widget(StartupScreen(name='startup'))
        screen_manager.add_widget(Startup1Screen(name='startup1'))
        screen_manager.add_widget(Startup2Screen(name='startup2'))
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(SignupScreen(name='signup'))
        screen_manager.add_widget(DashboardScreen(name='dashboard'))
        #screen_manager.add_widget(AnotherScreen(name='another_screen'))
        screen_manager.current = "startup"

        return screen_manager

class BaseScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        running_app = MDApp.get_running_app()
        self.md_bg_color = running_app.theme_cls.backgroundColor

class LoginScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags) 

class StartupScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

class Startup1Screen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

class Startup2Screen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

class SignupScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

class DashboardScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

    def toggle_nav_drawer(self):
        self.ids.top_app_bar.ids.nav_drawer.toggle_nav_drawer()

    def item_selected(self, text):
        print(f'Item selected: {text}')

if __name__ == "__main__":
    MyApp().run()
