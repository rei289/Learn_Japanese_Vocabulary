# Import libraries
import pandas as pd
import numpy as np
import random

# Import kivy libraries
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.metrics import dp


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT

#MDBottomNavigationItem MDApp
class Table(MDBottomNavigationItem):

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)

    def load_table(self, *args):
        # Layout
        self.layout = AnchorLayout()
        # Pandas dataframe
        df = pd.read_csv('/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')
        df = df.replace(np.nan, '')
        df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        dff = df.values.tolist()

        lst = []
        for i in range(len(dff)):
            # lst.append(str(i))
            lst.append(tuple(dff[i]))

        self.data_table = MDDataTable(
            size_hint=(1,1),
            use_pagination=True,
            column_data=[
                # ("Number", dp(20)),
                ("漢字", dp(10)),
                ("言葉", dp(10)),
                ("読み方", dp(35)),
                ("英語", dp(30)),
                ("意味", dp(60)),
                ("例文", dp(60))
            ],
            row_data=lst
        )
        # data_table.bind(on_row_press=self)
        self.add_widget(self.data_table)
        return self.layout

    def on_enter(self):
        self.load_table()




