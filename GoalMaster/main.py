# main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from db.database import Database

# Importing our screen modules
from screens.login_screen import LoginScreen
from screens.startup_screen import StartupScreen 
#from screens.goal_screen import GoalScreen
#from screens.tracker_screen import TrackerScreen
#from screens.piggybag_screen import PiggybagScreen
#from screens.history_screen import HistoryScreen

# Load the Kivy language file
KV = 'goalmaster.kv'

class GoalMasterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'  # Setting the primary color theme
        screen_manager = ScreenManager()
        # Adding screens to the screen manager
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(StartupScreen(name='startup'))
        #screen_manager.add_widget(GoalScreen(name='goal'))
        #screen_manager.add_widget(TrackerScreen(name='tracker'))
        #screen_manager.add_widget(PiggybagScreen(name='piggybag'))
        #screen_manager.add_widget(HistoryScreen(name='history'))

        # Initialize the database
        self.database = Database('goalmaster.db')

        # Add screens to the screen manager
        screen_manager.add_widget(LoginScreen(name='login', app=self))
        #screen_manager.add_widget(GoalScreen(name='goal', app=self))
        # ... (add other screens similarly)

        return screen_manager
    
    def on_stop(self):
        # Close the database connection when the app stops
        self.database.close()

# Running the app
if __name__ == '__main__':
    GoalMasterApp().run()
