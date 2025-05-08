import glob
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def get_directory_subfolders(
    input_root_folder: Folders,
    looks_into_subfolders: bool = True,
) -> list:
    subfolders = list()

    recursive_globs_pattern = (
        "/**/*"
        if looks_into_subfolders
        else "/*"
    )

    file_system_object_paths = glob.glob(
        pathname=input_root_folder.absolute_path_string
        + recursive_globs_pattern,
        recursive=True,
    )

    for (
        file_system_object_path
    ) in file_system_object_paths:
        __add_subfolder(
            file_system_object_path=file_system_object_path,
            subfolders=subfolders,
        )

    return subfolders


def __add_subfolder(
    file_system_object_path: str,
    subfolders: list,
) -> None:
    path = Path(file_system_object_path)

    if path.is_dir():
        folder = Folders(
            absolute_path_string=file_system_object_path,
        )

        subfolders.append(folder)
