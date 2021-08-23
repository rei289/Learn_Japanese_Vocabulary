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

# from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT

# Import code from different code
from Application.Japanese_Vocab_input import Input
from Application.Japanese_Vocab_flashcard import FlashCard
from Application.Japanese_Vocab_fix import Fix
from Application.Japanese_Vocab_table import Table

LabelBase.register(DEFAULT_FONT, 'Arial Unicode copy.ttf')


#
# class ContentNavigationDrawer(BoxLayout):
#     screen_manager = ObjectProperty()
#     nav_drawer = ObjectProperty()


class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Teal
        kv = Builder.load_file("Application/my.kv")
        return kv


if __name__ == "__main__":
    MyMainApp().run()
