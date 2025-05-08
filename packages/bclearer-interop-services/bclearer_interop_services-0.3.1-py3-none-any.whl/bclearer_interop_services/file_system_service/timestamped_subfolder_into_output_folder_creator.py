import os

from bclearer_interop_services.file_system_service.new_folder_if_required_creator import (
    create_new_folder_if_required,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


def create_timestamped_subfolder_into_output_folder(
    output_root_folder: Folders,
) -> Folders:
    current_date_for_timestamped_subfolder = (
        now_time_as_string_for_files()
    )

    output_timestamped_subfolder_name = "_".join(
        (
            current_date_for_timestamped_subfolder,
            "out",
        ),
    )

    output_timestamped_subfolder_path = os.path.join(
        output_root_folder.absolute_path_string,
        output_timestamped_subfolder_name,
    )

    create_new_folder_if_required(
        parent_output_folder=output_root_folder,
        new_folder_name=output_timestamped_subfolder_name,
    )

    output_timestamped_subfolder = Folders(
        absolute_path_string=output_timestamped_subfolder_path,
    )

    return output_timestamped_subfolder
