import sys
from textual.app import App, ComposeResult

from src.editor import Editor
from src.file_io import ensure_base_content


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.editor = Editor(id="editor")

    def on_mount(self):
        startTextArea = self.editor.text_areas[self.editor.current_text_area]
        startTextArea.focus()
        startTextArea.read_only = True

    def compose(self) -> ComposeResult:
        yield self.editor


if __name__ == "__main__":
    if not ensure_base_content():
        sys.exit(1)

    app = MyApp()
    app.run()
    sys.exit(app.return_code)
