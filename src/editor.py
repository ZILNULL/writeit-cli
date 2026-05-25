from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
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
        Binding("a", "new_text_area"),
    ]

    DEFAULT_CSS = """
    VerticalScroll {
        display: none;
    }

    VerticalScroll TextAreaExt {
        height: 50%;
    }
    """

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.mode = "n"
        self.current_text_area = 0
        self.edit_position = None
        self.editor_header = HeaderWI()
        self.text_areas = [TextAreaExt(id="input0")]
        self.editor_footer = FooterWI()
        self.vertical_container = VerticalScroll()
        self.horizontal_container = Horizontal(
            self.text_areas[0],
            self.vertical_container,
        )

    def compose(self) -> ComposeResult:
        yield self.editor_header
        yield self.horizontal_container
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

    def action_new_text_area(self) -> None:
        new_input = len(self.text_areas)
        self.text_areas.append(TextAreaExt(id=f"input{new_input}"))
        self.vertical_container.mount(self.text_areas[new_input])
        self.current_text_area = new_input
        self.text_areas[self.current_text_area].focus()
        self.text_areas[self.current_text_area].read_only = True

        if self.vertical_container.styles.display == "none":
            self.vertical_container.styles.display = "block"

    @on(Input.Submitted)
    def action_command_submit(self) -> None:
        if self.mode != "c":
            return

        command = self.editor_footer.command_input.value
        match command:
            case "q":
                self.app.exit(return_code=0)
            case "w":
                self.editor_footer.command_input.value = ""
                currentTextArea = self.text_areas[self.current_text_area]
                destination = write_to_file(
                    currentTextArea.text, currentTextArea.filename
                )
                currentTextArea.filename = destination
                self.editor_header.label.content = f"Content written to {destination}"


if __name__ == "__main__":
    editor = Editor()
