import os
from datetime import datetime


def write_to_file(text: str, filename: str | None = None) -> str:
    try:
        os.makedirs("content", exist_ok=True)
        filename_base = (
            datetime.today().strftime("%Y-%m-%d_%H:%M:%S") + ".md"
            if filename is None
            else filename
        )
        filename = os.path.join("content", filename_base)

        with open(filename, "w") as f:
            f.write(text)

        return filename_base
    except Exception as e:
        raise Exception(e)
