import pytest

from src.main import MyApp
from src.textarea import TextAreaExt


@pytest.mark.asyncio
async def test_init_focus():
    app = MyApp()
    async with app.run_test() as pilot:
        assert app.focused == app.query_one("#input1")


@pytest.mark.asyncio
async def test_focus_textarea():
    app = MyApp()
    async with app.run_test() as pilot:
        assert app.focused == app.query_one("#input1", TextAreaExt)
        assert app.query_one("#input1", TextAreaExt).read_only

        await pilot.press("i")
        assert app.focused == app.query_one("#input1", TextAreaExt)
        assert not app.query_one("#input1", TextAreaExt).read_only

        await pilot.press("escape")
        assert app.focused == app.query_one("#input1", TextAreaExt)
        assert app.query_one("#input1", TextAreaExt).read_only


@pytest.mark.asyncio
async def test_moving_bindings():
    app = MyApp()
    async with app.run_test() as pilot:
        input_widget = app.query_one("#input1", TextAreaExt)
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
