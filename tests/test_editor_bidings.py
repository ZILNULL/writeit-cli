import pytest

from src.editor import Editor
from src.main import MyApp


@pytest.mark.asyncio
async def test_init_focus():
    app = MyApp()
    async with app.run_test():
        assert app.focused == app.query_one("#input0")


@pytest.mark.asyncio
async def test_focus_textarea():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        input_widget = editor_widget.text_areas[editor_widget.current_text_area]
        assert app.focused == input_widget
        assert input_widget.read_only

        await pilot.press("i")
        assert app.focused == input_widget
        assert not input_widget.read_only

        await pilot.press("escape")
        assert app.focused == input_widget
        assert input_widget.read_only


@pytest.mark.asyncio
async def test_moving_bindings():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        input_widget = editor_widget.text_areas[editor_widget.current_text_area]
        await pilot.press("i")
        assert not input_widget.read_only

        await pilot.press("h", "e", "l", "l", "o", "enter", "w", "o", "r", "l", "d")
        assert input_widget.text == "hello\nworld"

        location_to_check = input_widget.get_cursor_left_location()
        await pilot.press("escape", "h")
        assert input_widget.cursor_location == location_to_check

        location_to_check = input_widget.get_cursor_up_location()
        await pilot.press("k")
        assert input_widget.cursor_location == location_to_check

        location_to_check = input_widget.get_cursor_down_location()
        await pilot.press("j")
        assert input_widget.cursor_location == location_to_check

        location_to_check = input_widget.get_cursor_right_location()
        await pilot.press("l")
        assert input_widget.cursor_location == location_to_check


@pytest.mark.asyncio
async def test_command_switching():
    app = MyApp()
    async with app.run_test() as pilot:
        editor_widget = app.query_one("#editor", Editor)
        input_widget = editor_widget.text_areas[editor_widget.current_text_area]
        footer_widget = editor_widget.editor_footer

        await pilot.press("i")
        assert not input_widget.read_only
        assert editor_widget.mode == "i"

        await pilot.press("escape")
        assert editor_widget.mode == "n"
        assert input_widget.read_only

        await pilot.press(":")
        assert editor_widget.mode == "c"
        assert app.focused == footer_widget.command_input
