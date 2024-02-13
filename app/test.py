from kivy.core import window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

from kivy.lang import Builder
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog



window.Window.clearcolor = (0, 0, 0, 1)
window.Window.size = (360, 600)


KV = '''
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        hint_text: "Enter a Todo"

    MDTextField:
        hint_text: "Enter Time"


MDFloatLayout:

'''


class Content(BoxLayout):
    pass

class Example(MDApp):
    
    dialog = None
    def build(self):
        
        tool_bar = MDToolbar(
            title= "Todo",
            pos_hint ={'center_y':.95}
        )
        
        
    
        data_tables = MDDataTable(
            size_hint=(1,.9),
            check = True,
            column_data=[
                ("", dp(10)),
                ("Content", dp(35)),
                ("Time", dp(15)),
            ]
        )

        add_button = MDIconButton(
            md_bg_color = self.theme_cls.primary_color,
            icon = 'plus',
            pos_hint = {'center_x':.5},
            on_press = self.show_confirmation_dialog
        )
        
        
        screen = Screen()
        screen.add_widget(tool_bar)
        screen.add_widget(data_tables)
        screen.add_widget(add_button)
        screen.add_widget(Builder.load_string(KV))
        return screen


    def show_confirmation_dialog(self, obj):

        def close_dilog(obj):
            self.dialog.dismiss()
        
        def use_input(obj):
            print('heare i wan to print the Todo and time')

        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press = close_dilog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press = use_input
                    ),
                ],
            )
        self.dialog.open()


Example().run()