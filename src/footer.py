from textual.app import ComposeResult
from textual.widgets import Input
from textual.widget import Widget


class FooterWI(Widget, can_focus=True):
    DEFAULT_CSS = """
    FooterWI {
        height: 2;
        dock: bottom;
    }
    """

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.command_input = Input(id="command", placeholder="Command here...")

    def compose(self) -> ComposeResult:
        yield self.command_input
