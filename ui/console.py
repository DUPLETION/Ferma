from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.core.text import Label
from kivy.uix.boxlayout import BoxLayout


class Console(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readonly = True
        self.multiline = True
        self.background_color = (0.1, 0.1, 0.1, 1)
        self.foreground_color = (0, 1, 0, 1)
        self.font_size = 12

    def append_text(self, text, color=(0, 1, 0, 1)):
        self.text += str(text) + "\n"
        self.cursor = (len(self.text), len(self.text) - 1)

    def clear(self):
        self.text = ""
