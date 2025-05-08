import glob
import os.path

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def get_all_files_of_extension_from_folder(
    folder: Folders,
    dot_extension_string: str,
    looks_into_subfolders: bool = True,
) -> list:
    list_of_files_of_extension = list()

    recursive_globs_pattern = (
        "/**/*"
        if looks_into_subfolders
        else "/*"
    )

    file_system_object_paths = glob.glob(
        pathname=folder.absolute_path_string
        + recursive_globs_pattern
        + dot_extension_string,
        recursive=True,
    )

    for (
        file_system_object_path
    ) in file_system_object_paths:
        list_of_files_of_extension = __add_file_of_specific_extension(
            file_system_object_path=file_system_object_path,
            dot_extension_string=dot_extension_string,
            list_of_files_of_extension=list_of_files_of_extension,
        )

    return list_of_files_of_extension


def __add_file_of_specific_extension(
    file_system_object_path: str,
    dot_extension_string: str,
    list_of_files_of_extension: list,
) -> list:
    if not file_system_object_path.endswith(
        dot_extension_string,
    ):
        return (
            list_of_files_of_extension
        )

    if not os.path.isdir(
        file_system_object_path,
    ):
        file = Files(
            absolute_path_string=file_system_object_path,
        )

        list_of_files_of_extension.append(
            file,
        )

    return list_of_files_of_extension
