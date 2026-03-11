from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty


class CodeEditor(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = True
        self.background_color = (0.05, 0.05, 0.15, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.font_size = 14
        self.font_name = "monospace"
        self.tab_width = 4

    def insert_text(self, substring, from_undo=False):
        if substring == "\n":
            line_start = self.text.rfind("\n", 0, self.cursor_col) + 1
            line = self.text[line_start:self.cursor_col]
            indent = len(line) - len(line.lstrip())
            substring = "\n" + " " * indent
        elif substring == "\t":
            substring = " " * self.tab_width
        return super().insert_text(substring, from_undo)
