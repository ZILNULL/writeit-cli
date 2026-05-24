from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget

from src.textarea import TextAreaExt


class Editor(Widget, can_focus=True):
    BINDINGS = [
        Binding("escape", "normal_mode"),
        Binding("i", "insert_mode"),
        Binding("h", "move_left"),
        Binding("j", "move_down"),
        Binding("k", "move_up"),
        Binding("l", "move_right"),
    ]

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.current_text_area = 1

    def compose(self) -> ComposeResult:
        yield TextAreaExt(id="input1")

    def action_normal_mode(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.read_only = True

    def action_insert_mode(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.read_only = False

    def action_move_left(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.move_cursor_relative(0, -1, record_width=True)

    def action_move_right(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.move_cursor_relative(0, 1, record_width=True)

    def action_move_down(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.move_cursor_relative(1, 0, record_width=True)

    def action_move_up(self) -> None:
        currTextArea = self.query_one(f"#input{self.current_text_area}", TextAreaExt)
        currTextArea.move_cursor_relative(-1, 0, record_width=True)


if __name__ == "__main__":
    editor = Editor()
