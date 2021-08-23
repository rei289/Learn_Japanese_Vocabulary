# Import libraries
import pandas as pd
import numpy as np
import random

# Import kivy libraries
from kivy.app import App
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


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT



class FlashCard(MDBottomNavigationItem):
    # Variables
    ind = ObjectProperty(None)
    wd = StringProperty()
    op = StringProperty()

    # Pandas dataframe
    df = pd.read_csv('/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')

    # Get rid of the divider
    position = df["英語"] == '-'
    indx_s = df.index[position].tolist()[0]
    df = df.drop(df.index[indx_s])
    df = df.sort_index().reset_index(drop=True)

    # Index of the csv file
    ind_c = len(df.index)

    def __init__(self, **kwargs):
        super(FlashCard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # Window.bind(on_key_down=self._on_keyboard_down)

        self.lst = random.sample(range(FlashCard.ind_c), FlashCard.ind_c)
        self.ind = 0

        self.wd = ''

        self.i = self.lst[self.ind]

        if pd.isna(FlashCard.df.at[self.i, "言葉"]) == True:
            self.wd = FlashCard.df.loc[self.i, "漢字"]
        else:
            self.wd = FlashCard.df.loc[self.i, "言葉"]

    def refresh_button(self):
        self.lst = random.sample(range(FlashCard.ind_c), FlashCard.ind_c)
        self.ind = 0

        self.op = ''

        self.i = self.lst[self.ind]
        if pd.isna(FlashCard.df.at[self.i, "言葉"]) == True:
            self.wd = FlashCard.df.loc[self.i, "漢字"]
        else:
            self.wd = FlashCard.df.loc[self.i, "言葉"]

    def previous_button(self):
        self.ind -= 1
        self.i = self.lst[self.ind]

        self.op = ''

        if pd.isna(FlashCard.df.at[self.i, "言葉"]) == True:
            self.wd = FlashCard.df.loc[self.i, "漢字"]
        else:
            self.wd = FlashCard.df.loc[self.i, "言葉"]

    def check_button(self):
        if pd.isna(FlashCard.df.at[self.i, "言葉"]) == True:
            on_kun = FlashCard.df.loc[self.i, "読み方 (音|訓)"].split('\n')
            self.op = "読み方：" + on_kun[0] + '\n' + '　　　　' + on_kun[1] + "\n英語：" + FlashCard.df.loc[self.i, "英語"]

        else:
            self.op = "読み方：" + FlashCard.df.loc[self.i, "読み方 (音|訓)"] + "\n英語：" + FlashCard.df.loc[self.i, "英語"]

    def next_button(self):
        self.ind += 1
        self.i = self.lst[self.ind]

        self.op = ''

        if pd.isna(FlashCard.df.at[self.i, "言葉"]) == True:
            self.wd = FlashCard.df.loc[self.i, "漢字"]
        else:
            self.wd = FlashCard.df.loc[self.i, "言葉"]

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.previous_button()

        if keycode[1] == 'right':
            self.next_button()

        if keycode[1] == 'down':
            self.check_button()

        if keycode[1] == 'up':
            self.refresh_button()