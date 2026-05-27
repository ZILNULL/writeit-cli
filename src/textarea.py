from textual.binding import Binding
from textual.widgets import TextArea


class TextAreaExt(TextArea):
    BINDINGS = [
        Binding("tab", "insert_tab"),
    ]

    DEFAULT_CSS = """
    TextAreaExt {
        border: round #C1C6C7;
    }

    TextAreaExt:focus {
        border: round #70FFD9;
    }
    """

    def __init__(self, id: str | None = None, filename: str | None = None):
        super().__init__(id=id)
        self.language = "markdown"
        self.filename = filename

    def action_insert_tab(self) -> None:
        if not self.read_only:
            self.insert("\t")


if __name__ == "__main__":
    textarea = TextAreaExt()
