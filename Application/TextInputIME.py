__all__ = ('TextInputIME', )


from kivy.uix.textinput import TextInput
from kivy.base import EventLoop
from kivy.core.window import Window


from kivy.properties import StringProperty


class TextInputIME(TextInput):
    testtext = StringProperty()


    def __init__(self, **kwargs):
        super(TextInputIME, self).__init__(**kwargs)
        EventLoop.window.bind(on_textedit = self._on_textedit)

    #     # Testing
    #     self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    #     self._keyboard.bind(on_key_down=self._on_keyboard_down)
    # # Testing
    # def _keyboard_closed(self):
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    #
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'enter':
    #         self.testtext = self.testtext.strip("\n")

    # This is fine
    def _on_textedit(self, window, text):
        #print(text)
        self.testtext = text

