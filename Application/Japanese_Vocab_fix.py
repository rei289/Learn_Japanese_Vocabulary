# Import libraries
import pandas as pd
import numpy as np
import random

# Import kivy libraries
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT


class Fix(MDBottomNavigationItem):
    # Variables
    wd = ObjectProperty(None)
    # kj = ObjectProperty(None)
    # kb = ObjectProperty(None)
    fx = ObjectProperty(None)
    ind = ObjectProperty(None)
    sy = StringProperty()
    eg = StringProperty()
    mn = StringProperty()
    rb = StringProperty()
    ip = ObjectProperty(None)

    dd1 = ObjectProperty()
    dd2 = ObjectProperty()

    # Pandas dataframe
    df = pd.read_csv('/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')

    def __init__(self, **kwargs):
        super(Fix, self).__init__(**kwargs)
        self.ind = 0
        self.sy = ''
        self.eg = ''
        self.mn = ''
        self.rb = ''

    def refresh_button(self):
        self.wd.text = ''
        self.fx.text = ''
        self.ind = 0
        self.sy = ''
        self.eg = ''
        self.mn = ''
        self.rb = ''

    def refresh_input_button(self):
        self.ip.text = ''

    # First dropdown menu
    def first_dropdown(self):
        dd1 = self.ids.dd1
        # For the drop down menu
        items = [{"viewclass": "OneLineListItem",
                  "text": "漢字",
                  "on_release": self.kanji,
                  },
                 {"viewclass": "OneLineListItem",
                  "text": "言葉",
                  "on_release": self.kotoba,
                  }]
        self.menu1 = MDDropdownMenu(caller=dd1, items=items, width_mult=4)
        self.menu1.open()

    # Second dropdown menu
    def second_dropdown(self):
        dd2 = self.ids.dd2
        # For the drop down menu

        items = [{"viewclass": "OneLineListItem",
                  "text": "読み方",
                  "on_release": self.yomikata,
                  },
                 {"viewclass": "OneLineListItem",
                  "text": "英語",
                  "on_release": self.eigo,
                  },
                 {"viewclass": "OneLineListItem",
                  "text": "意味",
                  "on_release": self.imi,
                  },
                 {"viewclass": "OneLineListItem",
                  "text": "例文",
                  "on_release": self.reibun,
                  }]
        self.menu2 = MDDropdownMenu(caller=dd2, items=items, width_mult=4)
        self.menu2.open()

    # If the word you are trying to change is a kanji
    def kanji(self):
        # self.kj.text = 'y'
        # self.kb.text = ''
        position = Fix.df["漢字"] == self.wd.text
        self.ind = Fix.df.index[position].tolist()[0]
        print(self.ind)

    # If the word you are trying to change is a word
    def kotoba(self):
        # self.kj.text = ''
        # self.kb.text = 'y'
        position = Fix.df["言葉"] == self.wd.text
        self.ind = Fix.df.index[position].tolist()[0]

    # If you want to fix its pronunciation
    def yomikata(self):
        self.fx.text = str(Fix.df.loc[self.ind, "読み方 (音|訓)"])
        self.sy = 'y'
        self.eg = ''
        self.mn = ''
        self.rb = ''

    # If you want to fix its translation to english
    def eigo(self):
        self.fx.text = str(Fix.df.loc[self.ind, "英語"])
        self.sy = ''
        self.eg = 'y'
        self.mn = ''
        self.rb = ''

    # If you want to fix its meaning in japanese
    def imi(self):
        self.fx.text = str(Fix.df.loc[self.ind, "意味"])
        self.sy = ''
        self.eg = ''
        self.mn = 'y'
        self.rb = ''

    # If you want to fix its example in japanese
    def reibun(self):
        self.fx.text = str(Fix.df.loc[self.ind, "例文"])
        self.sy = ''
        self.eg = ''
        self.mn = ''
        self.rb = 'y'

    def submit_button(self):
        if self.sy == 'y':
            Fix.df.at[self.ind, "読み方 (音|訓)"] = self.fx.text

        elif self.eg == 'y':
            Fix.df.at[self.ind, "英語"] = self.fx.text

        elif self.mn == 'y':
            Fix.df.at[self.ind, "意味"] = self.fx.text

        elif self.rb == 'y':
            Fix.df.at[self.ind, "例文"] = self.fx.text

        Fix.df.drop(Fix.df.columns[Fix.df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

    def confirm_button(self):

        Fix.df.to_csv(r'/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')
