# フル画面を解除して画面の幅と高さを設定
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '150')

import ctypes
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.utils import platform
from kivy.base import EventLoop
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import escape_markup
from kivy.uix.widget import Widget


def set(family, *filenames):
    for f in filenames:
        try:
            LabelBase.register(family, f)
            break
        except BaseException:
            pass


resource_add_path('/Library/Fonts')
set(DEFAULT_FONT, 'Arial Unicode copy.ttf')

dll = ctypes.cdll.LoadLibrary('./ime_operator.dll')

dll.getComposition.restype = ctypes.c_char_p
dll.getEnterdString.restype = ctypes.c_char_p  # POINTER(ctypes.c_char)


class TextInputIME(TextInput):

    composition_string = StringProperty()
    sdl_composition = StringProperty()
    composition_window = ObjectProperty()

    def __init__(self, **kwargs):

        super(TextInputIME, self).__init__(**kwargs)

        self.disable_on_textedit = (False, False)
        self.is_openIME = False
        self.old_cursor_color = self.cursor_color
        self.old_composition = ''

        EventLoop.window.bind(on_textedit=self._on_textedit)

    def _on_textedit(self, _, value):

        self.sdl_composition = value
        self.is_openIME = bool(dll.getIsOpenIME())

        try:
            entered_text = dll.getEnterdString().decode('cp932')
            composition_string = dll.getComposition().decode('cp932')
        except UnicodeError:
            print('failed to decode IME information')

        if composition_string != '\n\n':
            self.composition_string = composition_string
        else:
            self.composition_string = ''

        if (entered_text != '\n\n' and self.is_openIME and
                self.old_composition != value):
            index = self.cursor_index()
            self.text = self.text[:index - 1] + entered_text + self.text[index:]
            self.composition_string = ''
            self.old_composition = value
            return None

        self.old_composition = value

    def insert_text(self, substring, from_undo=False):

        if substring == self.sdl_composition:
            return None
        else:
            return super(TextInputIME, self).insert_text(substring, from_undo)

    def keyboard_on_key_down(self, window, keycode, text, modifiers, dt=0):

        cursor_operations = {'left', 'up', 'right', 'down', 'backspace', 'tab'}
        self.composition_cursor_index = len(self.composition_string)

        if keycode[1] == 'left':
            self.composition_cursor_index -= 1

        if keycode[1] == 'right':
            self.composition_cursor_index += 1

        if keycode[1] in cursor_operations and self.composition_string:
            return None

        return super(
            TextInputIME,
            self).keyboard_on_key_down(
            window,
            keycode,
            text,
            modifiers)

    def on_composition_string(self, _, value):

        if self.composition_string:
            self.cursor_color = (0, 0, 0, 0)
        else:
            self.cursor_color = self.old_cursor_color

        if not dll.getIsOpenIME():
            return

        # 下線を引くための処理です。
        self.composition_window.text = '[u]' + value + '[/u]'


class CompositionLabel(Label):

    textinput = ObjectProperty()

    def __init__(self, **kwargs):
        super(CompositionLabel, self).__init__(**kwargs)


class MultiLanguageTextInput(Widget):

    # プロパティの追加
    text = StringProperty()

    # ボタンをクリック時
    def on_command(self, **kwargs):
        self.text = self.ids.textinput.text


if __name__ == '__main__':

    class TestApp(App):
        def build(self):
            return MultiLanguageTextInput()

    TestApp().run()


