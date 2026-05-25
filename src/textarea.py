from textual.binding import Binding
from textual.widgets import TextArea


class TextAreaExt(TextArea):
    BINDINGS = [
        Binding("tab", "insert_tab"),
    ]

    def __init__(self, id: str | None = None, filename: str | None = None):
        super().__init__(id=id)
        self.language = "markdown"
        self.filename = filename

    def action_insert_tab(self) -> None:
        if not self.read_only:
            self.insert("\t")


if __name__ == "__main__":
    textarea = TextAreaExt()
