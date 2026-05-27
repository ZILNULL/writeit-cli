from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input

from src.editor_layout import EditorLayout
from src.footer import FooterWI
from src.header import HeaderWI
from src.textarea import TextAreaExt
from src.file_io import obtain_full_path, write_to_file


class Editor(Widget, can_focus=True):
    BINDINGS = [
        Binding("escape", "normal_mode"),
        Binding("i", "insert_mode"),
        Binding("h", "move_cursor('h')"),
        Binding("j", "move_cursor('j')"),
        Binding("k", "move_cursor('k')"),
        Binding("l", "move_cursor('l')"),
        Binding(":", "command_mode"),
        Binding("enter", "command_submit"),
        Binding("a", "new_text_area"),
        Binding("ctrl+h", "move_to_left_area"),
        Binding("ctrl+j", "move_to_down_area"),
        Binding("ctrl+k", "move_to_up_area", priority=True),
        Binding("ctrl+l", "move_to_right_area"),
        Binding("alt+h", "shift_to_left_area", priority=True),
        Binding("alt+j", "shift_to_down_area", priority=True),
        Binding("alt+k", "shift_to_up_area", priority=True),
        Binding("alt+l", "shift_to_right_area", priority=True),
    ]

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self.mode = "n"
        self.current_text_area = 0
        self.previous_text_area = None

        self.editor_header = HeaderWI()
        self.text_areas = [TextAreaExt()]
        self.editor_footer = FooterWI()
        self.horizontal_container = EditorLayout(self.text_areas)

    def compose(self) -> ComposeResult:
        yield self.editor_header
        yield self.horizontal_container
        yield self.editor_footer

    async def rebuild_containers(self) -> None:
        await self.horizontal_container.update_content(self.text_areas)

    def focus_area(self, index: int | None = None) -> None:
        if len(self.text_areas) == 0 or index is None:
            self.horizontal_container.focus()
            return

        self.current_text_area = index
        self.text_areas[index].read_only = True
        self.text_areas[index].focus()

    def unfocus_area(self, index: int) -> None:
        if len(self.text_areas) == 0:
            return

        self.text_areas[index].read_only = True

    async def delete_area(self, index: int) -> None:
        del self.text_areas[index]
        await self.horizontal_container.update_content(self.text_areas)

        if self.current_text_area >= len(self.text_areas):
            if len(self.text_areas) == 0:
                self.current_text_area = 0
            elif self.current_text_area == len(self.text_areas):
                self.current_text_area -= 1

    def insert_mode_area(self, index: int) -> None:
        self.focus_area(index)
        self.text_areas[index].read_only = False

    def change_mode(self, new_mode: str) -> bool:
        if len(self.text_areas) == 0 and new_mode == "i":
            return False

        self.mode = new_mode
        return True

    # -------------------------------
    # Actions
    # -------------------------------
    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if len(self.text_areas) == 0 or self.current_text_area is None:
            not_allowed = [
                "insert_mode",
                "move_cursor",
                "move_to_left_area",
                "move_to_right_area",
                "move_to_up_area",
                "move_to_down_area",
                "shift_to_left_area",
                "shift_to_right_area",
                "shift_to_up_area",
                "shift_to_down_area",
            ]
            if action in not_allowed:
                return False
        if self.mode != "n":
            not_allowed = [
                "move_cursor",
                "move_to_left_area",
                "move_to_up_area",
                "move_to_down_area",
                "move_to_right_area",
                "shift_to_up_area",
                "shift_to_left_area",
                "shift_to_right_area",
                "shift_to_down_area",
            ]
            if action in not_allowed:
                return False

        return True

    def action_normal_mode(self) -> None:
        self.focus_area(self.current_text_area)
        self.change_mode("n")

    def action_insert_mode(self) -> None:
        self.insert_mode_area(self.current_text_area)
        self.change_mode("i")

    def action_command_mode(self) -> None:
        commandWindow = self.editor_footer.command_input
        commandWindow.focus()
        self.change_mode("c")

    async def action_new_text_area(
        self, content: str | None = None, path: Path | None = None
    ) -> None:
        new_input = len(self.text_areas)
        text_area = TextAreaExt()
        if content is not None and path is not None:
            text_area.text = content
            text_area.filename = str(path)

        self.text_areas.append(text_area)
        await self.horizontal_container.update_content(self.text_areas)
        self.focus_area(new_input)

    def action_move_cursor(self, key: str) -> None:
        currTextArea = self.text_areas[self.current_text_area]
        match key:
            case "h":
                currTextArea.move_cursor_relative(0, -1)
            case "j":
                currTextArea.move_cursor_relative(1, 0, record_width=True)
            case "k":
                currTextArea.move_cursor_relative(-1, 0, record_width=True)
            case "l":
                currTextArea.move_cursor_relative(0, 1)
            case _:
                raise ValueError("Wrong key passed to action_move_cursor.")

    def action_move_to_left_area(self) -> None:
        if self.current_text_area == 0:
            return

        self.previous_text_area = self.current_text_area
        self.unfocus_area(self.current_text_area)
        self.focus_area(0)

    def action_move_to_right_area(self) -> None:
        if self.current_text_area != 0 or len(self.text_areas) == 1:
            return

        next_area = (
            self.previous_text_area if self.previous_text_area is not None else 1
        )
        self.previous_text_area = None
        self.unfocus_area(self.current_text_area)
        self.focus_area(next_area)

    def action_move_to_up_area(self) -> None:
        if self.current_text_area == 1 or self.current_text_area == 0:
            return

        self.unfocus_area(self.current_text_area)
        self.focus_area(self.current_text_area - 1)

    def action_move_to_down_area(self) -> None:
        if (
            self.current_text_area == len(self.text_areas) - 1
            or self.current_text_area == 0
        ):
            return

        self.unfocus_area(self.current_text_area)
        self.focus_area(self.current_text_area + 1)

    async def action_shift_to_left_area(self) -> None:
        if self.current_text_area == 0:
            return

        curr = self.current_text_area
        self.text_areas[0], self.text_areas[curr] = (
            self.text_areas[curr],
            self.text_areas[0],
        )
        await self.horizontal_container.update_content(self.text_areas)
        self.action_move_to_left_area()

    async def action_shift_to_right_area(self) -> None:
        if self.current_text_area != 0 or len(self.text_areas) == 1:
            return

        next_area = (
            self.previous_text_area if self.previous_text_area is not None else 1
        )
        self.text_areas[0], self.text_areas[next_area] = (
            self.text_areas[next_area],
            self.text_areas[0],
        )
        await self.horizontal_container.update_content(self.text_areas)
        self.action_move_to_right_area()

    async def action_shift_to_up_area(self) -> None:
        if self.current_text_area == 1 or self.current_text_area == 0:
            return

        curr = self.current_text_area

        self.text_areas[curr - 1], self.text_areas[curr] = (
            self.text_areas[curr],
            self.text_areas[curr - 1],
        )
        await self.horizontal_container.update_content(self.text_areas)
        self.action_move_to_up_area()

    async def action_shift_to_down_area(self) -> None:
        if (
            self.current_text_area == len(self.text_areas) - 1
            or self.current_text_area == 0
        ):
            return

        curr = self.current_text_area
        self.text_areas[curr + 1], self.text_areas[curr] = (
            self.text_areas[curr],
            self.text_areas[curr + 1],
        )
        await self.horizontal_container.update_content(self.text_areas)
        self.action_move_to_down_area()

    # -------------------------------
    # Commands
    # -------------------------------
    @on(Input.Submitted)
    async def action_command_submit(self) -> None:
        if self.mode != "c":
            return

        command_full = self.editor_footer.command_input.value
        command_split = command_full.split(" ", maxsplit=1)
        command = command_split[0]
        args = command_split[1] if len(command_split) > 1 else None

        self.editor_footer.command_input.value = ""
        match command:
            case "q":
                if len(self.text_areas) == 0:
                    self.app.exit(0)
                    return
                await self.delete_area(self.current_text_area)
                self.editor_footer.system_messages.content = "Deleted buffer."
            case "qa":
                self.app.exit(0)
            case "w":
                currentTextArea = self.text_areas[self.current_text_area]
                filename = args if args is not None else currentTextArea.filename
                destination = write_to_file(currentTextArea.text, filename)
                currentTextArea.filename = destination
                self.editor_footer.system_messages.content = (
                    f"Content written to {str(obtain_full_path(destination))}"
                )

        self.action_normal_mode()


if __name__ == "__main__":
    editor = Editor()
