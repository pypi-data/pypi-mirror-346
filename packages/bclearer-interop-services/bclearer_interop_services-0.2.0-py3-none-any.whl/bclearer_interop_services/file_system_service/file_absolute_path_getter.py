import os
from typing import Optional


def get_file_absolute_path(
    drive_relative_path: str,
    file_name: str,
) -> str | None:
    for root, dirs, files in os.walk(
        drive_relative_path,
    ):
        if file_name in files:
            return os.path.join(
                root,
                file_name,
            )

    return None
