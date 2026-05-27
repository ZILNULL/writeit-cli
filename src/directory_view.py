import os
from pathlib import Path
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import DirectoryTree

from src.confirm_screen import ConfirmScreen
from src.file_io import BASE_CONTENT_PATH, create_empty_file, delete_file


class DirectoryWI(Widget, can_focus=True):
    BINDINGS = [
        Binding("a", "append_file"),
        Binding("r", "delete_file"),
    ]

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

    def action_delete_file(self) -> None:
        if (
            self.directorytree.cursor_node is None
            or self.directorytree.cursor_node.data is None
        ):
            return

        message = f"Do you want to delete the file at: {str(self.directorytree.cursor_node.data.path)}?"
        self.app.push_screen(
            ConfirmScreen(message, "confirm_button", self.delete_file_resolve)
        )

    def delete_file_resolve(self) -> None:
        if (
            self.directorytree.cursor_node is None
            or self.directorytree.cursor_node.data is None
        ):
            return

        delete_file(self.directorytree.cursor_node.data.path)
        self.reload()

    def action_append_file(self) -> None:
        if (
            self.directorytree.cursor_node is None
            or self.directorytree.cursor_node.data is None
        ):
            return

        folder = self.directorytree.cursor_node.data.path
        if os.path.exists(folder) and os.path.isfile(folder):
            folder = folder.parent

        message = f"Insert name for new file at: {folder} (ESC to cancel)"
        self.app.push_screen(
            ConfirmScreen(
                message,
                "text_input",
                self.append_file_resolve,
                kwargs={"folder": folder},
            )
        )

    def append_file_resolve(
        self, folder: Path | None = None, text_input: str | None = None
    ) -> None:
        if folder is None:
            return

        filename = text_input if text_input is not None else "newfile.md"
        create_empty_file(folder, filename)
        self.reload()
