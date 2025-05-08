from bclearer_interop_services.file_system_service.file_system_objects_from_paths_getter import (
    get_file_system_objects_from_paths,
)
from bclearer_interop_services.file_system_service.files_of_extension_from_folder_getter import (
    get_all_files_of_extension_from_folder,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def get_all_files_from_file_system_object_paths(
    file_system_object_paths: list,
    base_root_path: str = "",
    dot_extension_string: str = "",
    looks_into_subfolders: bool = True,
) -> list:
    file_system_objects = get_file_system_objects_from_paths(
        paths=file_system_object_paths,
        base_root_path=base_root_path,
    )

    primary_grammar_files = list()

    for primary_grammar_file_system_object in (file_system_objects):
        if isinstance(
            primary_grammar_file_system_object,
            Files,
        ):
            primary_grammar_files.append(
                primary_grammar_file_system_object,
            )

        elif isinstance(
            primary_grammar_file_system_object,
            Folders,
        ):
            primary_grammar_files.extend(
                get_all_files_of_extension_from_folder(
                    folder=primary_grammar_file_system_object,
                    dot_extension_string=dot_extension_string,
                    looks_into_subfolders=looks_into_subfolders,
                ),
            )

    return primary_grammar_files
