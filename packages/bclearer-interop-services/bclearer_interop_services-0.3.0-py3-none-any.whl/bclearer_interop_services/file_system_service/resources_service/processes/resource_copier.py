import importlib
import os
import shutil

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def copy_resource_and_rename(
    database_template_folder_path: str,
    database_template_name: str,
    target_folder: Folders,
    new_name: str,
) -> Files:
    module = importlib.import_module(
        name=database_template_folder_path,
    )

    module_path_string = (
        module.__path__[0]
    )

    resource_full_file_name = (
        os.path.join(
            module_path_string,
            database_template_name,
        )
    )

    target_full_file_name = os.path.join(
        target_folder.absolute_path_string,
        new_name,
    )

    shutil.copy(
        src=resource_full_file_name,
        dst=target_full_file_name,
    )

    return Files(
        absolute_path_string=target_full_file_name,
    )
