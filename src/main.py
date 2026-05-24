from textual.app import App, ComposeResult

from src.editor import Editor
from src.textarea import TextAreaExt


class MyApp(App):
    def on_mount(self):
        startTextArea = self.query_one("#input1", TextAreaExt)
        startTextArea.focus()
        startTextArea.read_only = True

    def compose(self) -> ComposeResult:
        yield Editor(id="editor")


if __name__ == "__main__":
    app = MyApp()
    app.run()
