import os
import pathlib
import time


class PathProperties:
    def __init__(
        self,
        input_file_system_object_path: str,
    ):
        self.length = ""

        if os.path.isfile(
            input_file_system_object_path,
        ):
            self.length = os.path.getsize(
                filename=input_file_system_object_path,
            )

        # TODO: to check folder extensions
        self.extension = pathlib.Path(
            input_file_system_object_path,
        ).suffix

        self.creation_time = time.ctime(
            os.path.getctime(
                filename=input_file_system_object_path,
            ),
        )

        self.last_access_time = time.ctime(
            os.path.getatime(
                filename=input_file_system_object_path,
            ),
        )

        self.last_write_time = time.ctime(
            os.path.getmtime(
                filename=input_file_system_object_path,
            ),
        )
