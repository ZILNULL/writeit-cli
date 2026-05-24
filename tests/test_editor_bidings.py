import pytest

from src.main import MyApp
from src.editor import Editor
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
