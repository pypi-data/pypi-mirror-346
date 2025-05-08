import os.path

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.relative_path_to_absolute_converter import (
    convert_relative_path_to_absolute,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def get_file_system_objects_from_paths(
    paths: list,
    base_root_path: str = "",
) -> list:
    file_system_objects = list()

    if not os.path.exists(
        base_root_path,
    ):
        raise FileNotFoundError

    for path in paths:
        file_system_object = get_file_system_object_from_path(
            path=path,
            base_root_path=base_root_path,
        )

        if not isinstance(
            file_system_object,
            Folders,
        ):
            raise TypeError

        if not os.path.exists(
            file_system_object.absolute_path_string,
        ):
            raise FileNotFoundError

        if file_system_object:
            file_system_objects.append(
                file_system_object,
            )

    return file_system_objects


def get_file_system_object_from_path(
    path: str,
    base_root_path: str = "",
):
    absolute_path = convert_relative_path_to_absolute(
        input_path=path,
        base_root_path=base_root_path,
    )

    if os.path.exists(
        absolute_path,
    ) and os.path.isdir(absolute_path):
        file_system_object = Folders(
            absolute_path_string=absolute_path,
        )

    elif os.path.exists(
        absolute_path,
    ) and os.path.isfile(absolute_path):
        file_system_object = Files(
            absolute_path_string=absolute_path,
        )

    elif not os.path.exists(
        absolute_path,
    ):
        log_message(
            message=absolute_path
            + " - Does not exist",
        )

        return None

    else:
        log_message(
            message=absolute_path
            + " - Is not a file nor a folder",
        )

        return None

    return file_system_object
