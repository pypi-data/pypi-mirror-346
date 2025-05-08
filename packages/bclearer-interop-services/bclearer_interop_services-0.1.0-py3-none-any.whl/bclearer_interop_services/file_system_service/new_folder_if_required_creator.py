import os

from bclearer_interop_services.file_system_service.new_folder_creator import (
    create_new_folder,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def create_new_folder_if_required(
    parent_output_folder: Folders,
    new_folder_name: str,
) -> None:
    new_folder_path = os.path.join(
        parent_output_folder.absolute_path_string,
        new_folder_name,
    )

    if os.path.exists(new_folder_path):
        return

    create_new_folder(
        parent_folder_path=parent_output_folder.absolute_path_string,
        new_folder_name=new_folder_name,
    )
