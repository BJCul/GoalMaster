from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty

from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawerItem, MDNavigationDrawerItemTrailingText
)

Window.size = (360, 640)

KV = '''
<DrawerItem>
    active_indicator_color: "#e7e4c0"

    MDNavigationDrawerItemLeadingIcon:
        icon: root.icon
        theme_icon_color: "Custom"
        icon_color: "#4a4939"

    MDNavigationDrawerItemText:
        text: root.text
        theme_text_color: "Custom"
        text_color: "#4a4939"


<DrawerLabel>
    adaptive_height: True
    padding: "18dp", 0, 0, "12dp"

    MDNavigationDrawerItemLeadingIcon:
        icon: root.icon
        theme_icon_color: "Custom"
        icon_color: "#4a4939"
        pos_hint: {"center_y": .5}

    MDNavigationDrawerLabel:
        text: root.text
        theme_text_color: "Custom"
        text_color: "#4a4939"
        pos_hint: {"center_y": .5}
        padding: "6dp", 0, "16dp", 0
        theme_line_height: "Custom"
        line_height: 0


MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDBoxLayout:
                    orientation: "vertical"

                    MDTopAppBar:
                        type: 'small'

                        MDTopAppBarLeadingButtonContainer:

                            MDActionTopAppBarButton:
                                icon: "menu"
                                md_icon_color: "005B96"
                                #pos_hint: {"center_x": .10, "center_y": .95} 
                                on_release: nav_drawer.set_state("toggle")

                        MDTopAppBarTitle:
                            text: "My Account"
                            theme_text_color: "Custom"
                            text_color: "005B96"
                            #pos_hint: {"center_x": .5, "center_y": .95} 
                            font_style: "Title"
                            role: "large"
                            bold: True
                            pos_hint: {"center_x": .5}

                    MDFloatLayout: 

                        MDCard:
                            style: "outlined"
                            pos_hint: {"center_x": .50, "center_y": .82}
                            padding: "4dp"
                            size_hint: None, None
                            size: "300dp", "150dp"

                            MDRelativeLayout:

                                MDLabel:
                                    text: "See all"                          
                                    # icon: "dots-vertical"
                                    pos: "230dp", "51dp"
                                    font_style: "Label"
                                    role: "medium"

                                MDLabel:
                                    text: "Tracker"
                                    adaptive_size: True
                                    color: "grey"
                                    pos: "15dp", "113dp"
                                    bold: True

                                MDNavigationDrawerDivider:
                                    pos: "0dp", "100dp"
                                    color: "black"

                                MDLabel:
                                    text: "Total Savings:"
                                    adaptive_size: True
                                    color: "grey"
                                    pos: "15dp", "55dp"
                                    font_style: "Title"
                                    role: "small"

                                    MDLabel:
                                        text: "Php 500"
                                        adaptive_size: True
                                        color: "blue"
                                        bold: True
                                        pos: "15dp", "30dp"
                                        font_style: "Title"
                                        role: "large"
                                    

                        MDCard:
                            style: "outlined"
                            pos_hint: {"center_x": .50, "center_y": .52}
                            padding: "4dp"
                            size_hint: None, None
                            size: "300dp", "150dp"

                            MDRelativeLayout:
                                
                                MDLabel:
                                    text: "See all"                          
                                    # icon: "dots-vertical"
                                    pos: "230dp", "51dp"
                                    font_style: "Label"
                                    role: "medium"

                                MDLabel:
                                    text: "Piggy Bank"
                                    adaptive_size: True
                                    color: "grey"
                                    pos: "15dp", "113dp"
                                    bold: True

                                MDNavigationDrawerDivider:
                                    pos: "0dp", "100dp"
                                    color: "black"

                                MDLabel:
                                    text: "Allowance:"
                                    adaptive_size: True
                                    color: "grey"
                                    pos: "15dp", "55dp"
                                    font_style: "Title"
                                    role: "small"

                                    MDLabel:
                                        text: "Php 500"
                                        adaptive_size: True
                                        color: "blue"
                                        bold: True
                                        pos: "15dp", "30dp"
                                        font_style: "Title"
                                        role: "large" 

                




        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(5), dp(5), 0

            MDNavigationDrawerMenu:

                DrawerItem:
                    icon: "plus"
                    text: "Add Account"

                MDNavigationDrawerDivider:
                    
                DrawerItem:
                    icon: "account"
                    text: "Edit Account"
                
                MDNavigationDrawerDivider:
                    
                DrawerItem:
                    icon: "pin"
                    text: "Pinned Transaction"
                
                MDNavigationDrawerDivider:
                    
                DrawerItem:
                    icon: "flag"
                    text: "Add Goal"
                
                MDNavigationDrawerDivider:
                    
                DrawerItem:
                    icon: "exit-to-app"
                    text: "Log out"
'''


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


class Dashboard(MDApp):
    def build(self):
        return Builder.load_string(KV)


Dashboard().run()