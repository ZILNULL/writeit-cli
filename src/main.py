from collections.abc import Callable
import sys
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DirectoryTree

from src.confirm_screen import ConfirmScreen
from src.directory_view import DirectoryWI
from src.editor import Editor
from src.file_io import (
    ensure_base_content,
    obtain_full_path,
    obtain_relative_path,
    read_file,
)


class MyApp(App):
    BINDINGS = [
        Binding("s", "switch_view", priority=True),
        Binding("d", "toggle_directory"),
    ]

    DEFAULT_CSS = """
    App {
        background: darkblue;
    }

    #directory {
        dock: left;
        width: 25%;
        display: none;
    }
    """

    def __init__(self):
        super().__init__()
        self.editor = Editor(id="editor")
        self.directory = DirectoryWI(id="directory")

    def on_mount(self):
        self.editor.action_normal_mode()

    def compose(self) -> ComposeResult:
        yield self.editor
        yield self.directory

    def add_confirm_window(
        self,
        message: str,
        type_confirm: str,
        function: Callable,
        args: list = [],
        kwargs: dict = {},
    ) -> None:
        self.push_screen(ConfirmScreen(message, type_confirm, function, args, kwargs))

    # ----------------------------------------
    # Actions
    # ----------------------------------------
    def action_toggle_directory(self):
        if self.directory.styles.display == "block":
            self.directory.styles.display = "none"
            self.editor.action_normal_mode()
            return

        self.directory.styles.display = "block"
        self.directory.give_focus()

    def action_switch_view(self):
        if self.directory.focused:
            self.directory.focused = False
            self.editor.action_normal_mode()
            return

        if self.directory.styles.display == "none":
            return

        self.directory.give_focus()

    # ----------------------------------------
    # Handlers
    # ----------------------------------------
    @on(DirectoryTree.FileSelected)
    async def directory_file_selected(
        self, message: DirectoryTree.FileSelected
    ) -> None:
        content = read_file(message.path)
        relative = obtain_relative_path(message.path)
        await self.editor.action_new_text_area(content=content, path=relative)


if __name__ == "__main__":
    if not ensure_base_content():
        sys.exit(1)

    app = MyApp()
    app.run()
    sys.exit(app.return_code)
