from collections.abc import Callable
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Label


class ConfirmScreen(Screen):
    BINDINGS = [
        Binding("escape", "close_screen"),
    ]

    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    Button {
        width: 100%;
    }

    Button#confirm {
        background: green;
    }

    Button#cancel {
        background: red;
    }

    Input {
        width: 100%;
        column-span: 2;
    }
    """

    def __init__(
        self,
        message: str,
        type_confirm: str,
        function: Callable,
        args: list = [],
        kwargs: dict = {},
    ):
        super().__init__()
        self.message = message
        self.type_confirm = type_confirm
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.confirm_prompt: list[Widget] = []

    def resolve_confirm_prompt(self) -> None:
        self.confirm_prompt = []
        if self.type_confirm == "text_input":
            self.confirm_prompt.append(Input(id="text_confirm"))
        elif self.type_confirm == "confirm_button":
            self.confirm_prompt.append(Button("Yes", id="confirm"))
            self.confirm_prompt.append((Button("No", id="cancel")))

    def compose(self) -> ComposeResult:
        self.resolve_confirm_prompt()
        yield Grid(
            Label(self.message, id="question"), *self.confirm_prompt, id="dialog"
        )

    def action_close_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.function(*self.args, **self.kwargs)
            self.app.pop_screen()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text_input = event.value
        self.kwargs["text_input"] = text_input
        self.function(*self.args, **self.kwargs)
        self.app.pop_screen()
