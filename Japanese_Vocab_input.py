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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from TextInputIME import TextInputIME

from kivy.core.text import LabelBase, DEFAULT_FONT

class Input(MDBottomNavigationItem):
    # Variables
    wd = ObjectProperty(None)
    yn = ''
    sy = ObjectProperty(None)
    eg = ObjectProperty(None)
    mn = ObjectProperty(None)
    rb = ObjectProperty(None)
    ip = ObjectProperty(None)

    dd = ObjectProperty()

    # Pandas dataframe
    df = pd.read_csv('/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')

    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)

    def buttonClicked(self):

        self.wd.text = self.ids["wd"].text
        self.sy.text = self.ids["sy"].text
        self.eg.text = self.ids["eg"].text
        self.mn.text = self.ids["mn"].text
        self.rb.text = self.ids["rb"].text

    def refresh_button(self):
        self.wd.text = ''
        self.sy.text = ''
        self.eg.text = ''
        self.mn.text = ''
        self.rb.text = ''

    def refresh_input_button(self):
        self.ip.text = ''

    def open_dropdown(self):
        dd = self.ids.dd
        # For the drop down menu
        items = [{"viewclass": "OneLineListItem",
                        "text": "Yes",
                       "on_release": self.kanji_yes_button,
                       },
                      {"viewclass": "OneLineListItem",
                       "text": "No",
                       "on_release": self.kanji_no_button,
                      }]
        self.menu = MDDropdownMenu(caller=dd, items=items, width_mult=4)
        self.menu.open()

    def kanji_yes_button(self):

        self.yn = "y"
        self.sy.text = "[音]　\n[訓]　"

    def kanji_no_button(self):

        self.yn = "n"
        self.sy.text = ""

    def submit_button(self):

        # Get rid of new line
        if "\n" in self.wd.text:
            self.wd.text = self.wd.text.strip("\n")
        if "\n" in self.eg.text:
            self.eg.text = self.eg.text.strip("\n")
        if "\n" in self.mn.text:
            self.mn.text = self.mn.text.strip("\n")
        if "\n" in self.rb.text:
            self.rb.text = self.rb.text.strip("\n")

        #
        # # If nothing is entered
        # if self.wd.text == "":
        #     self.wd.text = "NaN"
        # if self.sy.text == "":
        #     self.sy.text = "NaN"
        # if self.eg.text == "":
        #     self.eg.text = "NaN"
        # if self.mn.text == "":
        #     self.mn.text = "NaN"
        # if self.rb.text == "":
        #     self.rb.text = "NaN"

        # CHECK TO SEE IF WORDS WERE ALREADY ENTERED
        # length of sheet
        duplicate = 0
        ln = len(Input.df.index)
        for i in range(ln):
            if self.wd.text == Input.df['漢字'][i]:
                duplicate = 1
            elif self.wd.text == Input.df['言葉'][i]:
                duplicate = 1
        if duplicate == 0:
            # create a list
            ls = []
            if self.yn == "y":
                lst = [self.wd.text, '']
                # on_kun = self.sy.text.split('|')
                # # 音読み
                # on = on_kun[0]
                # # 訓読み
                # kun = on_kun[1]
                # sy = "[音]　" + on + "\n" + "[訓]　" + kun
                lst.append(self.sy.text)
            else:
                lst = ['', self.wd.text]
                lst.append(self.sy.text)

            lst.append(self.eg.text)
            lst.append(self.mn.text)
            lst.append(self.rb.text)

            ls.append(lst)
            # SORT OUT WORDS
            # index of separation
            position = Input.df['英語'] == '-'
            indx = Input.df.index[position].tolist()[0]

            nindx = indx - 0.5
            # APPEND
            # if word is a single kanji
            if self.yn == 'y':
                t_in = nindx
                df2 = pd.DataFrame(ls, columns=["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"], index=[nindx])
                Input.df = FirstWindow.df.append(df2, ignore_index=False)
                Input.df = FirstWindow.df.sort_index().reset_index(drop=True)
                # see if any words from below separation can be grouped
                dff = Input.df["言葉"]
                for i in range(indx + 1, ln + 1):
                    if self.wd.text == dff[i][0]:
                        # locate the row
                        rw = Input.df.loc[i]
                        # convert to a list
                        nlst = rw.values.tolist()
                        # append to proper section
                        df3 = pd.DataFrame([nlst], columns=["Unnamed: 0", "漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"],
                                           index=[indx + 0.5])
                        Input.df = Input.df.append(df3, ignore_index=False)
                        Input.df = Input.df.sort_index().reset_index(drop=True)
                        # delete from original spot
                        Input.df = Input.df.drop(FirstWindow.df.index[i + 1])
                        Input.df = Input.df.sort_index().reset_index(drop=True)


            # if word
            else:
                # located index for all kanji
                lst_k = []
                ln = len(Input.df.index)
                for i in range(ln):
                    if pd.isnull(Input.df.loc[i, "言葉"]) == True:
                        lst_k.append(i)

                # append to the first kanji
                dff = Input.df["漢字"]
                for i in range(indx + 1):
                    if dff.loc[i] == self.wd.text[0]:
                        t_in = i
                        df2 = pd.DataFrame(ls, columns=["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"], index=[0.5 + i])
                        Input.df = Input.df.append(df2, ignore_index=False)
                        Input.df = Input.df.sort_index().reset_index(drop=True)
                        break

                    elif i == indx:
                        t_in = i
                        df2 = pd.DataFrame(ls, columns=["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"], index=[indx + 0.5])
                        Input.df = Input.df.append(df2, ignore_index=False)
                        Input.df = Input.df.sort_index().reset_index(drop=True)
                        break

            Input.df.drop(Input.df.columns[Input.df.columns.str.contains('unnamed', case=False)], axis=1,
                           inplace=True)

        else:
            Input.df.drop(Input.df.columns[Input.df.columns.str.contains('unnamed', case=False)], axis=1,
                           inplace=True)

        # Create popup window which shows added row
        layout = GridLayout(cols = 1)
        rv = str(Input.df.loc[t_in - 3:t_in + 3])
        review = Label(text = rv)
        layout.add_widget(review)

        popupWindow = Popup(title="Review added word", content=layout, size_hint=(None, None), size=(1000, 1000))

        popupWindow.open()
    def confirm_button(self):

        self.wd.text = ""
        self.yn = ""
        self.sy.text = ""
        self.eg.text = ""
        self.mn.text = ""
        self.rb.text = ""

        Input.df.to_csv(r'/Users/tsuyoshikatsuta/Desktop/japanese_vocab.csv')


