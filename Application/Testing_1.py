# Import libraries
import pandas as pd
import numpy as np
import random

# Import kivy libraries
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.metrics import dp


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager

from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT


# Import code from different code
from Japanese_Vocab_input import Input
from Japanese_Vocab_flashcard import FlashCard
from Japanese_Vocab_fix import Fix
from Japanese_Vocab_table import Table

LabelBase.register(DEFAULT_FONT, 'Arial Unicode copy.ttf')


#
# class ContentNavigationDrawer(BoxLayout):
#     screen_manager = ObjectProperty()
#     nav_drawer = ObjectProperty()


class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue" #Teal  
#         kvv = Builder.load_string('''
#         <ContentNavigationDrawer>:
#
#     ScrollView:
#
#         MDList:
#
#             OneLineListItem:
#                 text: "Screen 1"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 1"
#
#             OneLineListItem:
#                 text: "Screen 2"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 2"
#
#             OneLineListItem:
#                 text: "Screen 3"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 3"
#
#             OneLineListItem:
#                 text: "Screen 4"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 4"
# Screen:
#
#     MDToolbar:
#         id: toolbar
#         pos_hint: {"top": 1}
#         elevation: 10
#         title: "Japanese Vocab Learning"
#         left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
#
#     MDNavigationLayout:
#         x: toolbar.height
#
#         ScreenManager:
#             id: screen_manager
#
# # First screen
#             Screen:
#                 name: "scr 1"
#
#                 MDLabel:
#                     text: "Screen 1"
#                     halign: "center"
#
# # Second screen
#             Screen:
#                 name: "scr 2"
#
#                 MDLabel:
#                     text: "Screen 2"
#                     halign: "center"
#
# # Third Screen
#             Screen:
#                 name: "scr 3"
#
#                 MDLabel:
#                     text: "Screen 3"
#                     halign: "center"
# # Fourth Screen
#             Screen:
#                 name: "scr 4"
#
#                 MDLabel:
#                     text: "Screen 4"
#                     halign: "center"
#
#
#         MDNavigationDrawer:
#             id: nav_drawer
#
#             ContentNavigationDrawer:
#                 screen_manager: screen_manager
#                 nav_drawer: nav_drawer''')

        # For the table
        # Pandas dataframe
        # df = pd.read_csv('/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')
        # dff = df.values.tolist()
        #
        # lst = []
        # for i in range(len(dff)):
        #     lst.append(tuple(dff[i]))
        #
        # self.data_tables = MDDataTable(
        #     size_hint=(0.9,0.6),
        #     column_data=[
        #         ("漢字", dp(20)),
        #         ("言葉", dp(20)),
        #         ("読み方", dp(40)),
        #         ("英語", dp(40)),
        #         ("意味", dp(80)),
        #         ("例文", dp(80))
        #     ],
        #     row_data=lst
        # )
        # data_table.bind(on_row_press=self)
        # self.add_widget(data_table)


        kv = Builder.load_file("mynew.kv")
        return kv

    # def on_start(self):
    #     self.data_tables.open()

if __name__ == "__main__":
    MyMainApp().run()
