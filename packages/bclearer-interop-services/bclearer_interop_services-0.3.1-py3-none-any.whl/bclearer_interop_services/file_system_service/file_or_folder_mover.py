import os
import shutil

from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_objects import (
    BEngWorkspaceFileSystemObjects,
)


def move_file_or_folder_and_create_sub_folders(
    source_object: BEngWorkspaceFileSystemObjects,
    target_object: BEngWorkspaceFileSystemObjects,
):
    container_folder_string = (
        target_object.parent_absolute_path_string
    )

    if not os.path.exists(
        container_folder_string,
    ):
        os.makedirs(
            container_folder_string,
        )

    __move_file_or_folder(
        source_object=source_object,
        target_object=target_object,
    )


def move_file_or_folder_and_do_not_create_sub_folders(
    source_object: BEngWorkspaceFileSystemObjects,
    target_object: BEngWorkspaceFileSystemObjects,
):
    # return success-failure
    __move_file_or_folder(
        source_object=source_object,
        target_object=target_object,
    )


def __move_file_or_folder(
    source_object: BEngWorkspaceFileSystemObjects,
    target_object: BEngWorkspaceFileSystemObjects,
):
    # return success-failure
    shutil.move(
        src=source_object.absolute_path_string,
        dst=target_object.absolute_path_string,
    )
