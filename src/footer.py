from textual.app import ComposeResult
from textual.widgets import Input, Label
from textual.widget import Widget


class FooterWI(Widget, can_focus=True):
    DEFAULT_CSS = """
    FooterWI {
        height: 1;
        min-height: 1;
        dock: bottom;
        layout: horizontal;
    }

    FooterWI Input {
        height: 100%;
        width: 50%;
        margin: 0;
        border: none;
        color: white;
    }

    FooterWI Input:focus {
        height: 100%;
        padding: 0 1;
        margin: 0;
        border: none;
    }

    FooterWI Label {
        height: 100%;
        width: 50%;
        content-align-horizontal: right;
    }
    """

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.command_input = Input(id="command", placeholder="Command here...")
        self.system_messages = Label("")

    def compose(self) -> ComposeResult:
        yield self.command_input
        yield self.system_messages
