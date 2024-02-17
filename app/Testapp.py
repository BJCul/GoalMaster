from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogSupportingText, MDDialogContentContainer
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.button import MDButton, MDButtonText
import os
from kivymd.uix.dialog import MDDialog, MDDialogContentContainer, MDDialogButtonContainer, MDDialogHeadlineText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from database import MySQLdb
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawerItem, MDNavigationDrawerItemTrailingText
)
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel


Window.size = (360, 640)
Window.top = 100
Window.left = 1000

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("Testapp.kv")

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Steelblue"
        self.db  = MySQLdb()

        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(StartupScreen(name='startup'))
        self.screen_manager.add_widget(Startup1Screen(name='startup1'))
        self.screen_manager.add_widget(CreateGoalScreen(name='creategoal'))
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SignupScreen(name='signup'))
        self.screen_manager.add_widget(SignupScreen1(name='signup1'))
        self.screen_manager.add_widget(DashboardScreen(name='dashboard'))
        self.screen_manager.add_widget(CreateexpensesScreen(name='createexpenses'))
        self.screen_manager.add_widget(TrackerScreen(name='tracker'))
        self.screen_manager.add_widget(PiggyScreen(name='piggy'))
        self.screen_manager.add_widget(AccountScreen(name='account'))
        self.screen_manager.add_widget(HistoryScreen_Piggy(name='history_piggy'))
        self.screen_manager.add_widget(HistoryScreen_Tracker(name='history_tracker'))
        self.screen_manager.current = "startup"

        return self.screen_manager
    
    def switch_to_screen(self, screen_name):
        current_screen_name = self.screen_manager.current
        transition_direction = self.determine_transition_direction(current_screen_name, screen_name)
        self.screen_manager.transition = SlideTransition(direction=transition_direction)
        self.screen_manager.current = screen_name

    def determine_transition_direction(self, current_screen_name, target_screen_name):
        # Determine the transition direction based on the current screen and target screen
        if current_screen_name == 'login' and target_screen_name == 'dashboard':
            return 'left'
        elif current_screen_name == 'tracker' and target_screen_name == 'dashboard':
            return 'right'
        elif current_screen_name == 'piggy' and target_screen_name == 'dashboard':
            return 'right'
        elif current_screen_name == 'dashboard' and target_screen_name == 'tracker':
            return 'left'
        elif current_screen_name == 'dashboard' and target_screen_name == 'piggy':
            return 'left'
        elif current_screen_name == 'history_piggy' and target_screen_name == 'piggy':
            return 'down'
        elif current_screen_name == 'piggy' and target_screen_name == 'history_piggy':
            return 'up'
        elif current_screen_name == 'tracker' and target_screen_name == 'history_tracker':
            return 'up'
        elif current_screen_name == 'history_tracker' and target_screen_name == 'tracker':
            return 'down'
        else:
            # Default transition direction
            return 'left' 

    def on_stop(self):
        self.db.close_db_connection()


class BaseScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        running_app = MDApp.get_running_app()
        self.md_bg_color = running_app.theme_cls.backgroundColor

class StartupScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    
    def switch_to_dashboard(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('dashboard')

class Startup1Screen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)

class SignupScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db  = MySQLdb()
        
    def create_user(self):
        """creating a account"""
        name = self.ids.name.text 
        email = self.ids.email.text
        password = self.ids.password.text

        # Check if user input have info
        if email != '' and password != '' and name != '':
            if self.db.check_email(email) == False: # Check email in the db if exist, if not create user then return True
                self.db.create_user(name,email,password)
                self.ids.name.text=''
                self.ids.email.text = ''
                self.ids.password.text=''
                self.update_account_content(name, email)
                return True, self.successful_signup_popup(), print("do not exist")
            
            elif self.db.check_email(email) == True: # Pop up the email exist then return false
                self.email_exists_popup()
                return False

        else:
            self.invalid_popup()
    
    def update_account_content(self, name, email):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('account')
        trackerscreen.update_account_data(name, email)

    def invalid_popup(self):
        '''Pop up for invalid entries'''
        dialog = MDDialog(
            MDDialogSupportingText(
                text="Invalid Entries",
                halign="left",
            ),           
        )
        dialog.open()
    

    def successful_signup_popup(self):
        '''Pop up for invalid entries'''
        dialog = MDDialog(
            MDDialogSupportingText(
                text="You have successfully created an account. Want to Log in?",
                halign="left",
            ), 
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Create account again"),
                    style="text",
                    on_press=lambda *args: self.dismiss_dialog(dialog)

                ),
                MDButton(
                    MDButtonText(text="Log In"),
                    style="text",
                    on_press=lambda *args: self.goto_login(dialog)

                ),
                spacing="8dp",
                
            ),
            size_hint = (.9, None)
        )
        dialog.open()

    def email_exists_popup(self):
        '''Pop up when email entered already exists'''
        dialog = MDDialog (            
            MDDialogSupportingText(
                text="You have already have an account",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Try Again"),
                    style="text",
                    on_press=lambda *args: self.dismiss_dialog(dialog)

                ),
                MDButton(
                    MDButtonText(text="Log In"),
                    style="text",
                    on_press=lambda *args: self.goto_login(dialog)

                ),
                spacing="8dp",
                
            ),
            size_hint = (.9, None)
        )
        dialog.open()

    def dismiss_dialog(self, dialog):
        dialog.dismiss()
    
    def goto_login(self, dialog):
        self.manager.current = 'login'
        dialog.dismiss()

    def enable_signup_btn(self):
        self.ids.signupbtn.disabled = False

class SignupScreen1(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db  = MySQLdb()
        
    def create_user(self):
        """creating a account"""
        name = self.ids.name.text 
        email = self.ids.email.text
        password = self.ids.password.text

        # Check if user input have info
        if email != '' and password != '' and name != '':
            if self.db.check_email(email) == False: # Check email in the db if exist, if not create user then return True
                self.db.create_user(name,email,password)          
                self.ids.name.text=''
                self.ids.email.text = ''
                self.ids.password.text=''                
                return True, self.successful_signup_popup(), print("do not exist")
            
            elif self.db.check_email(email) == True: # Pop up the email exist then return false
                self.email_exists_popup()
                return False

        else:
            self.invalid_popup()

    def invalid_popup(self):
        '''Pop up for invalid entries'''
        dialog = MDDialog(
            MDDialogSupportingText(
                text="Invalid Entries",
                halign="left",
            ),           
        )
        dialog.open()
       

    def successful_signup_popup(self):
        '''Pop up for invalid entries'''
        dialog = MDDialog(
            MDDialogSupportingText(
                text="You have successfully created an account.",
                halign="left",
            ), 
            size_hint = (.9, None)
        )
        dialog.open()           

    def email_exists_popup(self):
        '''Pop up when email entered already exists'''
        dialog = MDDialog (            
            MDDialogSupportingText(
                text="You have already have an account",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Try Again"),
                    style="text",
                    on_press=lambda *args: self.dismiss_dialog(dialog)

                ),
                MDButton(
                    MDButtonText(text="Log In"),
                    style="text",
                    on_press=lambda *args: self.goto_login(dialog)

                ),
                spacing="8dp",
                
            ),
            size_hint = (.9, None)
        )
        dialog.open()

    def dismiss_dialog(self, dialog):
        dialog.dismiss()
    
    def goto_login(self, dialog):
        self.manager.current = 'login'
        dialog.dismiss()

    def enable_signup_btn(self):
        self.ids.signupbtn.disabled = False

class AccountScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags) 
        self.db  = MySQLdb()

        self.update_account_data

    def update_account_data(self, name, email):
        name_label = self.ids.name
        email_label = self.ids.email
       
        # Update the widget values
        name_label.text = f"{name}"
        email_label.text = f"{email}"
    
    def change_name(self):
        user_id = self.db.get_logged_in_userid()
        new_name = self.ids.name.text
        updated_name = self.db.change_account_name(user_id,new_name)
        print("Updated name:", updated_name)
        self.ids.name.text = new_name

    def change_email(self):
        user_id = self.db.get_logged_in_userid()
        new_email = self.ids.email.text
        updated_email = self.db.change_account_email(user_id,new_email)
        print("Updated email:", updated_email)
        self.ids.email.text = new_email
    
    def change_password(self):
        user_id = self.db.get_logged_in_userid()
        new_password = self.ids.password.text
        self.db.change_account_name(user_id,new_password)
        self.ids.password.text = new_password
        self.ids.password.password = True
    
class LoginScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags) 
        self.db  = MySQLdb()
        self.successful_login = False
        self.user_id = None
    
    def user_login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        # check if user has press the keep me logged in check box
        if self.ids.keepmeloggedin.active == True:    
            keep_me_logged = True
        else: 
            keep_me_logged = False
        # check if users has an account 
        if email != '' and password != '':
            userid_ = self.db.get_user(email, password, keep_me_logged)            
    
            # validate the user
            if userid_ == True:
                self.successful_login = True
                userid = self.db.get_users(email, password, keep_me_logged)

                print("User ID:", userid)
                userid1 = userid[0]
                userid2 = userid[1]
                print("Name:", userid1), print("Email:",userid2)
                
                users_info = self.db.get_users_info(userid1)

                name = users_info[0][0]
                email = users_info[0][1]

                print("Name:", name), print("Email:",email)
                self.update_account_content(name, email)

                self.ids.email.text = ''
                self.ids.password.text=''
                return True, print("login success")
                        
            elif userid_ == False:
                self.invalid_popup()
    
            else:
                self.invalid_popup()
        else:
            self.invalid_popup()

    def update_account_content(self, name, email):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('account')
        trackerscreen.update_account_data(name, email)

    def invalid_popup(self):
        '''Pop up for invalid entries'''
        dialog = MDDialog (
            MDDialogHeadlineText(
                text="Incorrect Username or Password",
                halign="left"
            ),
            MDDialogSupportingText(
                text="You have entered invalid details. Please try again.",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Try Again"),
                    style="text",
                    on_press=lambda *args: self.dismiss_dialog(dialog)

                ),
                MDButton(
                    MDButtonText(text="Sign Up"),
                    style="text", 
                    on_press = lambda *args: self.goto_signup(dialog)
                    
                ), 
                spacing="8dp",
            ),
            size_hint=(.95, .5)
        )
        dialog.open()
        
    def dismiss_dialog(self, dialog):
        dialog.dismiss()

    def goto_signup(self, dialog):
        self.manager.current = 'signup'
        dialog.dismiss()

class DashboardScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db = MySQLdb()

    def log_out(self):
        logout = self.db.log_out_user()
        if logout:
            print('Logout Success')
        else:
            print('Log out unsuccessful')

    def update_allowance_data(self):
        user_id = self.db.get_logged_in_userid() 
        goals = self.db.get_goals(user_id)   

        if goals:
            goal_record = goals[0]
            goal_id = goal_record[0]
            print("Goal:", goal_id)                                        # Extract the goal_id from the first goal record
            allowance = self.db.get_allowance(goal_id)           
            total_expenses = self.db.total_spending()
            
            if allowance and total_expenses:
                # Accessing the values directly from the tuples
                allowance_value = allowance[0][0] if allowance else 0
                total_expenses_value = total_expenses[0][0] if total_expenses else 0
                remaining_allowance = allowance_value - total_expenses_value
                
                allowance_label = self.ids.allowance  # Access the label widget
                allowance_label.text = f"₱ {remaining_allowance}"
            else:
                print("Error fetching allowance or total expenses.")
        else:
            print("No goals found for the user.")



    def toggle_nav_drawer(self):
        self.ids.top_app_bar.ids.nav_drawer.toggle_nav_drawer()

    def item_selected(self, text):
        print(f'Item selected: {text}')
    
    def switch_to_tracker(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('tracker')

    def switch_to_piggy(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('piggy')

class CreateGoalScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db  = MySQLdb()
    
    def add_goal(self):
        user_id = self.db.get_logged_in_userid()  
        goal_name = self.ids.goal_name.text
        goal_amount = self.ids.goal_amount.text
        goal_duration = self.ids.goal_duration.text 
        allowance = self.ids.allowance.text  
        if goal_name != '' and goal_amount != '' and goal_duration != '' and allowance != '':
            self.db.create_goals(user_id, goal_name, goal_amount, goal_duration, allowance)
            goals = self.db.get_goals(user_id)
            self.update_piggy_content()
            self.update_trackerscreen_content()
            self.update_dashboard_content()
            print('goal created successfully')
            if goals:
                print('created successfully')
            else: 
                print('goal not created')
        else: 
            print('Input the text fields')        

    def update_piggy_content(self):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('piggy')
        trackerscreen.update_piggy_data()
    
    def update_dashboard_content(self):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('dashboard')
        trackerscreen.update_dashboard_data()

    def update_trackerscreen_content(self):
        screen_manager = self.manager
        tracker = screen_manager.get_screen('tracker')
        tracker.update_allowance_data()



class DrawerLabel(MDBoxLayout):
    icon = StringProperty()
    text = StringProperty()
 

class DrawerItem(MDNavigationDrawerItem):
    icon = StringProperty()
    text = StringProperty()

    _trailing_text_obj = None

    def on_trailing_text(self, instance, value):
        self._trailing_text_obj = MDNavigationDrawerItemTrailingText(
            text=value,
            theme_text_color="Custom",
            text_color=self.trailing_text_color,
        )
        self.add_widget(self._trailing_text_obj)

    def on_trailing_text_color(self, instance, value):
        self._trailing_text_obj.text_color = value

class DialogScreen_Delete(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
     
    def cancel_dialog(self):
        print('closed')
        self.dismiss() 
    
    def confirm_exp(self):
        print('ehehehehehe')

class DialogScreen(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = MySQLdb()

    def cancel_dialog(self):
        print('closed')
        self.dismiss() 

    def confirm_exp(self):
        print('ehehehehehe')    

    def open_menu(self, item):
        menu_items = [
            {
                "text": "necessity",
                "on_release": lambda x="necessity": self.menu_callback(x),
            },
            {
                "text": "wants",
                "on_release": lambda x="wants": self.menu_callback(x), 
            }
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position= 'bottom')
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.category.text = text_item
        self.menu.dismiss() 

    def close_dialogbox(self):
        self.dialog = DialogScreen()
        self.dialog.dismiss()

    def add_expenses(self):
        user_id = self.db.get_logged_in_userid()
        expense_name = self.ids.expense_name.text
        expense_amount = self.ids.expense_amount.text

        if expense_name != '' and expense_amount != '':
            self.db.insert_expenses(user_id, expense_name, expense_amount)  # Inserting new expenses
            expenses = self.db.get_expenses(user_id)                        # getting the expenses based on current user_id
            self.update_trackerscreen_content()                             # clearing the expense_table 
            self.ids.expense_name.text = ''
            self.ids.expense_amount.text = ''
            # if expenses:
            #     # Switch to the TrackerScreen to update the display 
            #     app = MDApp.get_running_app()                
            #     app.switch_to_screen('tracker')
            # else:
            #     print("Expenses not recorded")
            #     return True, print("Expenses has been recorded")
            
    def update_trackerscreen_content(self):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('tracker')
        trackerscreen.update_expenses_data()

class TrackerScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = MySQLdb()


        self.update_expenses_data()         # Update content initially
        self.update_total_data()            # Update Total Expenses
        self.update_allowance_data()        # Update Allowance 
        #self.update_savings_data()         # Update Savings


    def update_savings_data(self):
        savings = self.ids.savings
        savings.text = f"Savings: ₱ {savings}"
    
    def update_allowance_data(self):
        user_id = self.db.get_logged_in_userid() 
        goals = self.db.get_goals(user_id)   
        
        print("Goal data:", goals)
        if goals:
            goal_record = goals[0]
            goal_id = goal_record[0]
            print("Goal:", goal_id)  # Extract the goal_id from the first goal record
            
            allowance = self.db.get_allowance(goal_id)           
            total_expenses = self.db.total_spending()
            
            if allowance and total_expenses:
                # Accessing the values directly from the tuples
                allowance_value = allowance[0][0] 
                total_expenses_value = total_expenses 
                remaining_allowance = allowance_value - int(total_expenses_value)
                
                allowance_label = self.ids.allowance  # Access the label widget
                allowance_label.text = f"₱ {remaining_allowance}"
            else:
                print("Error fetching allowance or total expenses.")
        else:
            print("No goals found for the user.")

    def update_total_data(self):
        expense_total_label = self.ids.expense_total
        total_spending_tuple = self.db.total_spending()

        total_spending = total_spending_tuple[0]

        expense_total_label.text = f"Total Expenses: ₱ {total_spending}"

    def update_expenses_data(self):
        self.update_total_data()
        self.update_allowance_data()
        user_id = self.db.get_logged_in_userid()
        items = self.db.get_expenses(user_id)
        
        expense_table = self.ids.expense_table
        expense_table.data = []

        if items is None:
            print("No items retrieved from the database.")
            return

        for expense_id, user_id, expense_name, expense_amount in items:
            expense_table.data.append(
                {
                    "viewclass": "MDLabel",
                    "text": f"{expense_id}                      {expense_name}            ₱ {expense_amount}",
                    "adaptive_height": True,
                    "theme_text_color": "Primary",
                    "font_style": "Body",
                    "role": "large"
                }
            )
        
        print("Data has been updated.")

    def switch_to_dashboard(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('dashboard')

    def switch_to_history_tracker(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('history_tracker')

class CreateexpensesScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db = MySQLdb()

    def add_expenses(self):
        user_id = self.db.get_logged_in_userid()
        expense_name = self.ids.expense_name.text
        expense_amount = self.ids.expense_amount.text

        if expense_name != '' and expense_amount != '':
            self.db.insert_expenses(user_id, expense_name, expense_amount) # Inserting new expenses
            expenses = self.db.get_expenses(user_id)              # getting the expenses based on current user_id
            self.update_trackerscreen_content()                   # clearing the expense_table 
            self.ids.expense_name.text = ''
            self.ids.expense_amount.text = ''
            if expenses:
                # Switch to the TrackerScreen to update the display 
                app = MDApp.get_running_app()                
                app.switch_to_screen('tracker')
            else:
                print("Expenses not recorded")
                return True, print("Expenses has been recorded")

    def open_menu(self):
        d = self.ids.drop_text    

    def delete_expense(self):
        expense_id = self.ids.expense_id.text
        
        if expense_id != '':
            expense_delete = self.db.delete_expenses(expense_id) # Delete new expenses
            self.update_trackerscreen_content()                   # updating the expense_table 
            self.ids.expense_id.text = ''

            if expense_delete:
                # Switch to the TrackerScreen to update the display 
                app = MDApp.get_running_app()                
                app.switch_to_screen('tracker')
            else:
                print("Expenses not Deleted")
                return True, print("Expenses has been recorded")       

    def update_trackerscreen_content(self):
        screen_manager = self.manager
        trackerscreen = screen_manager.get_screen('tracker')
        trackerscreen.update_expenses_data()


    def switch_to_dashboard(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('dashboard')

class PiggyScreen(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        self.db = MySQLdb()

        self.update_piggy_data()

    def update_piggy_data(self):
        user_id = self.db.get_logged_in_userid()    
        goals = self.db.get_goals(user_id)   
        
        # Update the goal name
        print("Goal data:", goals)
        if goals:
            goal_record = goals[0]
            print("Goal record:", goal_record) 

        # Goals containing record inside so typical indexing hindi gagana
        goal_id = goal_record[0]
        user_id = goal_record[1]
        _goal_name = goal_record[2]
        _goal_duration = goal_record[3]
        _goal_amount = goal_record[4]
        _allowance = goal_record[5]

        print("Goal:", goal_id, user_id, _goal_name, _goal_duration, _goal_amount, _allowance)

        if goal_record:
            goal_name = _goal_name # return the goal name
            updated_goal_name = goal_name.upper()  # Convert to uppercase
            
            # Update the goal name label
            goal_name_label = self.ids.goal_name
            goal_name_label.text = updated_goal_name
        
        try:
            if goals:
                goal_amount = _goal_amount
                formatted_goal_amount = "{:,.0f}".format(_goal_amount)
                goal_amount_label = self.ids.goal_amount
                goal_amount_label.text = formatted_goal_amount

        except ValueError:
            print("Invalid goal amount:", goal_amount)
            # Handle the case where the input is not a valid number

        # Update the goal duration
        try:
            if goals:
                goal_duration = _goal_duration
                formatted_deadline = _goal_duration.strftime("%B %d, %Y")
                goal_duration_label = self.ids.deadline
                goal_duration_label.text = formatted_deadline  # Update the goal duration label
                # goal_duration_label.text = f"{goal_duration}"
        except IndexError:
            print("Invalid goal duration or no goals found.")
            # Handle the case where the goal duration index is out of range or no goals are found
    
    def switch_to_dashboard(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('dashboard')
    
    def switch_to_history_piggy(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('history_piggy')

class HistoryScreen_Piggy(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    
    def switch_to_piggy(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('piggy')

class HistoryScreen_Tracker(BaseScreen):
    def __init__(self, **kwags):
        super().__init__(**kwags)
    
    def switch_to_tracker(self):
        app = MDApp.get_running_app()
        app.switch_to_screen('tracker')

    

if __name__ == "__main__":
    MyApp().run()


