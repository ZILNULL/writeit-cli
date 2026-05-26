from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label


class EditorLayout(Widget, can_focus=True):
    DEFAULT_CSS = """
    VerticalScroll {
        display: none;
    }

    VerticalScroll TextAreaExt {
        height: 50%;
    }
    """

    def __init__(self, text_areas: list[Widget] = []):
        super().__init__()
        self.text_areas = text_areas
        self.sub_editors = VerticalScroll()
        self.main_editor = Label("Editor goes here...")

        if len(self.text_areas) == 1:
            self.main_editor = self.text_areas[0]

        if len(self.text_areas) > 1:
            self.main_editor = self.text_areas[0]
            self.sub_editors = VerticalScroll(*self.text_areas[1:])

        self.layout_container = Horizontal(self.main_editor, self.sub_editors)

    def compose(self) -> ComposeResult:
        yield self.layout_container

    async def update_content(self, text_areas: list[Widget]):
        self.text_areas = text_areas
        self.main_editor = Label("Editor goes here...")

        if len(self.text_areas) == 1:
            self.main_editor = self.text_areas[0]
            self.sub_editors.styles.display = "none"

        if len(self.text_areas) > 1:
            self.main_editor = self.text_areas[0]
            self.sub_editors = VerticalScroll(*self.text_areas[1:])
            self.sub_editors.styles.display = "block"

        self.layout_container = Horizontal(self.main_editor, self.sub_editors)
        await self.recompose()


if __name__ == "__main__":
    editor_layout = EditorLayout()
