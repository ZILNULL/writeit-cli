import pytest

from src.editor import Editor
from src.main import MyApp


@pytest.mark.asyncio
async def test_insert_simple():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        input_widget = editor_widget.text_areas[editor_widget.current_text_area]
        await pilot.press("i")
        assert not input_widget.read_only

        await pilot.press("h", "e", "l", "l", "o", "enter", "w", "o", "r", "l", "d")
        assert input_widget.text == "hello\nworld"

        await pilot.press("tab")
        assert editor_widget.mode == "i"
        assert app.focused == input_widget
        assert input_widget.text == "hello\nworld\t"
