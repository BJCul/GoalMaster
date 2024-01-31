from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField




class TrackerScreen(MDBoxLayout):
    
    def add_item(self):
        self.item = input("Item No.: ")
        self.ids.list_items.add_widget(
                OneLineListItem(
                    text = self.item,
                    text_color = "#FFFFFF",
                    theme_text_color = "Custom"
                )
        )

    def show_dialog(self):
        textfield = MDTextField(
            hint_text="Enter text",
            helper_text="Helper text",
            helper_text_mode="on_focus",
        )
        #content = MDFlatButton(text="Your Dialog Content", on_release=self.close_dialog)
        dialog = MDDialog(title="Add Item")  #content=textfield)
        dialog.open()
        

    def close_dialog(self, instance):
        # Close the dialog
        instance.parent.parent.dismiss()


    


class tracker(MDApp):
    def build(self):
        return Builder.load_file("trackerscreen.kv")

    '''def on_start(self):
        for _ in range(50):
            self.root.ids.list_items.add_widget(
                OneLineListItem(
                    text = f'item {_}',
                    text_color = "#FFFFFF",
                    theme_text_color = "Custom"
                )
            )'''
    

    


if __name__ == '__main__':
    Window.size = (360, 636)
    Window.top = 30
    Window.left = 900
    tracker().run()