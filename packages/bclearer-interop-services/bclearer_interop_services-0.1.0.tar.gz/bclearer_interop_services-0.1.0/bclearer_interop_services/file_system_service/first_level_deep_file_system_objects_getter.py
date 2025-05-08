import glob

from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)


# TODO: To be promoted to somewhere else?
def get_first_level_children_file_system_object_paths(
    input_file_system_object: FileSystemObjects,
    extension_to_filter: str,
) -> list:
    input_file_system_object_paths = glob.glob(
        pathname=input_file_system_object.absolute_path_string
        + "/*"
        + extension_to_filter,
        recursive=True,
    )

    return (
        input_file_system_object_paths
    )
