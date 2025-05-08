import os

from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)


def get_file_system_object_mb_size(
    file_system_object: FileSystemObjects,
) -> float:
    file_system_object_mb_size = round(
        (
            os.path.getsize(
                filename=file_system_object.absolute_path_string,
            )
            / 1024
            / 1024
        ),
        3,
    )

    return file_system_object_mb_size
