import os

from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def rename_all_files_and_folders(
    folder: str,
    old: str,
    new: str,
):
    rename_all_folders(folder, old, new)

    rename_all_files(folder, old, new)


def rename_all_folders(
    root_folder: str,
    old: str,
    new: str,
):
    all_renames_were_successes = True

    for path, folders, files in os.walk(
        top=root_folder,
        topdown=False,
    ):
        for folder in folders:
            folder_path = os.path.join(
                path,
                folder,
            )

            rename_was_success = rename_filesystem_element(
                folder,
                folder_path,
                old,
                new,
            )

            all_renames_were_successes = (
                all_renames_were_successes
                and rename_was_success
            )

    if not all_renames_were_successes:
        rename_all_folders(
            root_folder,
            old,
            new,
        )


def rename_all_files(
    root_folder: str,
    old: str,
    new: str,
):
    for path, folders, files in os.walk(
        top=root_folder,
        topdown=False,
    ):
        for file in files:
            file_path = os.path.join(
                path,
                file,
            )

            rename_filesystem_element(
                file,
                file_path,
                old,
                new,
            )


def rename_filesystem_element(
    filesystem_element_name: str,
    filesystem_element_path: str,
    old: str,
    new: str,
) -> bool:
    if (
        old
        not in filesystem_element_name
    ):
        return True

    old_filesystem_element = (
        filesystem_element_path
    )

    new_filesystem_element = (
        filesystem_element_path.replace(
            old,
            new,
        )
    )

    log_message(
        message="Renaming "
        + old_filesystem_element
        + " to "
        + new_filesystem_element,
    )

    try:
        os.rename(
            old_filesystem_element,
            new_filesystem_element,
        )

        return True

    except FileNotFoundError:
        log_message(
            message="Failed because file was not found",
        )

        return False
