from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DirectoryTree

from src.file_io import BASE_CONTENT_PATH


class DirectoryWI(Widget, can_focus=True):
    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.directorytree = DirectoryTree(BASE_CONTENT_PATH)
        self.focused = False

    def compose(self) -> ComposeResult:
        yield self.directorytree

    def give_focus(self) -> None:
        self.directorytree.reload()
        self.directorytree.focus()
        self.focused = True

    def reload(self) -> None:
        self.directorytree.reload()

