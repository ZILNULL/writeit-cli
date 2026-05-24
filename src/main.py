from textual.app import App, ComposeResult

from src.editor import Editor


class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Editor()


if __name__ == "__main__":
    app = MyApp()
    app.run()
