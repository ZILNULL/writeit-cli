import sys
import os
from datetime import datetime


def write_to_file(text: str) -> str:
    try:
        os.makedirs("content", exist_ok=True)
        file_name = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
        file_name = os.path.join("content", file_name)

        with open(file_name, "w") as f:
            f.write(text)

        return file_name
    except Exception as e:
        sys.exit(1)
