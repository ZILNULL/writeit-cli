import os
from datetime import datetime
from pathlib import Path

BASE_PATH = Path.home() / ".writeit"
BASE_CONTENT_PATH = Path.home() / ".writeit" / "content"


def ensure_base_content() -> bool:
    os.makedirs(BASE_CONTENT_PATH, exist_ok=True)
    return True


def obtain_full_path(filename: Path | str) -> Path:
    resolved_path = (BASE_CONTENT_PATH / Path(filename)).resolve()
    if not resolved_path.is_relative_to(BASE_CONTENT_PATH):
        raise ValueError("Path given is outside of the working directory.")

    return resolved_path


def obtain_relative_path(path: Path | str) -> Path:
    try:
        resolved_path = obtain_full_path(path).resolve()
        if not resolved_path.is_relative_to(BASE_CONTENT_PATH):
            raise ValueError("Path given is outside of the working directory.")
        return resolved_path.relative_to(BASE_CONTENT_PATH)
    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        raise Exception(e)


def read_file(path: Path | str) -> str:
    try:
        path = obtain_full_path(path)
        with open(path, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        raise Exception(e)


def write_to_file(text: str, filename: str | None = None) -> str:
    try:
        filename_base = (
            datetime.today().strftime("%Y-%m-%d_%H:%M:%S") + ".md"
            if filename is None
            else filename
        )
        final_filename_base = Path(filename_base)
        full_path = obtain_full_path(final_filename_base)
        base_path = full_path.parent
        os.makedirs(base_path, exist_ok=True)

        with open(full_path, "w") as f:
            f.write(text)

        return filename_base
    except Exception as e:
        raise Exception(e)
