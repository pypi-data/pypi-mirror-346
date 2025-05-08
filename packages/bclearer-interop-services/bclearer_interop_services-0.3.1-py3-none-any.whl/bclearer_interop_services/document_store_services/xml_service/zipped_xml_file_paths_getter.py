import glob

from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)


def get_zipped_xml_file_paths(
    input_xml_file_system_object: FileSystemObjects,
) -> list:
    file_system_object_paths = glob.glob(
        pathname=input_xml_file_system_object.absolute_path_string
        + "/**/*.xml_service.gz",
        recursive=True,
    )

    return file_system_object_paths
