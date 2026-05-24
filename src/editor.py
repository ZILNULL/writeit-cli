from textual.app import ComposeResult
from textual.widget import Widget

from src.textarea import TextAreaExt


class Editor(Widget, can_focus=True):
    def compose(self) -> ComposeResult:
        yield TextAreaExt()


if __name__ == "__main__":
    editor = Editor()
