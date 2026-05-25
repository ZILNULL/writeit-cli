import sys
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input

from src.footer import FooterWI
from src.header import HeaderWI
from src.textarea import TextAreaExt
from src.file_io import write_to_file


class Editor(Widget, can_focus=True):
    BINDINGS = [
        Binding("escape", "normal_mode"),
        Binding("i", "insert_mode"),
        Binding("h", "move_left"),
        Binding("j", "move_down"),
        Binding("k", "move_up"),
        Binding("l", "move_right"),
        Binding(":", "command_mode"),
        Binding("enter", "command_submit"),
    ]

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.mode = "n"
        self.current_text_area = 0
        self.edit_position = None
        self.editor_header = HeaderWI()
        self.text_areas = [TextAreaExt(id="input0")]
        self.editor_footer = FooterWI()

    def compose(self) -> ComposeResult:
        yield self.editor_header
        for text_area in self.text_areas:
            yield text_area
        yield self.editor_footer

    def action_normal_mode(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.read_only = True
        currTextArea.focus()
        self.mode = "n"

    def action_insert_mode(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.read_only = False
        self.mode = "i"

    def action_command_mode(self) -> None:
        commandWindow = self.editor_footer.command_input
        commandWindow.focus()
        self.mode = "c"

    def action_move_left(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.move_cursor_relative(0, -1, record_width=True)

    def action_move_right(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.move_cursor_relative(0, 1, record_width=True)

    def action_move_down(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.move_cursor_relative(1, 0, record_width=True)

    def action_move_up(self) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        currTextArea.move_cursor_relative(-1, 0, record_width=True)

    @on(Input.Submitted)
    def action_command_submit(self) -> None:
        if self.mode != "c":
            return

        command = self.editor_footer.command_input.value
        match command:
            case "q":
                sys.exit(0)
            case "w":
                self.editor_footer.command_input.value = ""
                currentText = self.text_areas[self.current_text_area].text
                destination = write_to_file(currentText)
                self.editor_header.label.content = f"Content written to {destination}"


if __name__ == "__main__":
    editor = Editor()
