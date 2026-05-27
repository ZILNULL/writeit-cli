from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class HeaderWI(Widget):
    DEFAULT_CSS = """
    HeaderWI {
        height: 1;
        dock: top;
        layout: horizontal;
    }

    HeaderWI Label {
        height: 100%;
    }
    """

    def __init__(self):
        super().__init__()
        self.title = Label("WriteIt-CLI ")
        self.widgets: list[Widget] = []

    def compose(self) -> ComposeResult:
        yield self.title
        for widget in self.widgets:
            yield widget
