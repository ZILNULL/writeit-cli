from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class HeaderWI(Widget):
    DEFAULT_CSS = """
    HeaderWI {
        height: 1;
        dock: top;
    }
    """

    def __init__(self):
        super().__init__()
        self.label = Label("WriteIt-CLI")

    def compose(self) -> ComposeResult:
        yield self.label
