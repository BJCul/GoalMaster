from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from kivy.uix.boxlayout import BoxLayout


Window.size = (360, 640)

class LoginScreen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags) 
    pass

class StartupScreen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    pass

class Startup1Screen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    pass

class Startup2Screen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    pass

class SignupScreen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    pass

class DashboardScreen(Screen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

    def toggle_nav_drawer(self):
        self.ids.top_app_bar.ids.nav_drawer.toggle_nav_drawer()

    def item_selected(self, text):
        print(f'Item selected: {text}')
    
class ContentNavigationDrawer(BoxLayout):
        pass

screen_manager = ScreenManager()
# Adding screens to the screen manager
screen_manager.add_widget(StartupScreen(name='startup'))
screen_manager.add_widget(Startup1Screen(name='startup1'))
screen_manager.add_widget(Startup2Screen(name='startup2'))
screen_manager.add_widget(LoginScreen(name='login'))
screen_manager.add_widget(LoginScreen(name='signup'))
screen_manager.add_widget(DashboardScreen(name='dashboard'))


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        screen = Builder.load_file("Testapp.kv")
        return screen

if __name__ == "__main__":
    MyApp().run()
