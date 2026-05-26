import pytest

from src.editor import Editor
from src.main import MyApp


@pytest.mark.asyncio
async def test_create_new_area():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        input_widget = editor_widget.text_areas[0]
        assert app.focused == input_widget
        assert input_widget.read_only

        await pilot.press("a")
        input_widget = editor_widget.text_areas[1]
        assert editor_widget.current_text_area == 1
        assert app.focused == input_widget


@pytest.mark.asyncio
async def test_create_move_areas():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        await pilot.press("a", "a")
        input_widget = editor_widget.text_areas[2]
        assert editor_widget.current_text_area == 2
        assert app.focused == input_widget

        input_widget = editor_widget.text_areas[0]
        await pilot.press("ctrl+h")
        assert app.focused == input_widget

        await pilot.press("ctrl+h")
        assert app.focused == input_widget

        input_widget = editor_widget.text_areas[2]
        await pilot.press("ctrl+l")
        assert app.focused == input_widget

        await pilot.press("ctrl+l")
        assert app.focused == input_widget

        input_widget = editor_widget.text_areas[1]
        await pilot.press("ctrl+k")
        assert app.focused == input_widget

        input_widget = editor_widget.text_areas[2]
        await pilot.press("ctrl+j")
        assert app.focused == input_widget

        await pilot.press("ctrl+j")
        assert app.focused == input_widget

        input_widget = editor_widget.text_areas[1]
        await pilot.press("ctrl+k", "ctrl+k")
        assert app.focused == input_widget
