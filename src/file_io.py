import os
from datetime import datetime
from pathlib import Path

BASE_CONTENT_PATH = Path.home() / ".writeit" / "content"


def ensure_base_content() -> bool:
    os.makedirs(BASE_CONTENT_PATH, exist_ok=True)
    return True


def obtain_full_path(filename: str) -> str:
    return str(BASE_CONTENT_PATH / Path(filename))


def write_to_file(text: str, filename: str | None = None) -> str:
    try:
        filename_base = (
            datetime.today().strftime("%Y-%m-%d_%H:%M:%S") + ".md"
            if filename is None
            else filename
        )
        final_filename_base = Path(filename_base)
        full_path = BASE_CONTENT_PATH / Path(final_filename_base)
        base_path = full_path.parent
        os.makedirs(base_path, exist_ok=True)

        with open(full_path, "w") as f:
            f.write(text)

        return filename_base
    except Exception as e:
        raise Exception(e)
