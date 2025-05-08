from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.hierarchy_file_as_b_dataset_row_dictionary_getter import (
    get_hierarchy_file_as_b_dataset_row_dictionary,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.hierarchy_folder_information_as_b_dataset_row_dictionary_getter import (
    get_hierarchy_folder_information_as_b_dataset_row_dictionary,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def add_hierarchy_folder_to_b_dataset_format(
    hierarchy_file_system_object_register,
    hierarchy_folder: HierarchyFolders,
    b_dataset_format_dictionary: dict,
) -> dict:
    from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
        HierarchyFileSystemObjectRegisters,
    )

    if not isinstance(
        hierarchy_file_system_object_register,
        HierarchyFileSystemObjectRegisters,
    ):
        raise TypeError

    b_dataset_format_dictionary[
        hierarchy_folder.uuid
    ] = get_hierarchy_folder_information_as_b_dataset_row_dictionary(
        hierarchy_file_system_object_register=hierarchy_file_system_object_register,
        hierarchy_folder=hierarchy_folder,
    )

    for (
        child_object
    ) in (
        hierarchy_folder.child_hierarchy_file_system_objects
    ):
        if not isinstance(
            child_object,
            HierarchyFolders,
        ):
            b_dataset_format_dictionary[
                child_object.uuid
            ] = get_hierarchy_file_as_b_dataset_row_dictionary(
                hierarchy_file_system_object_register=hierarchy_file_system_object_register,
                hierarchy_file=child_object,
            )
        else:
            add_hierarchy_folder_to_b_dataset_format(
                hierarchy_file_system_object_register=hierarchy_file_system_object_register,
                hierarchy_folder=child_object,
                b_dataset_format_dictionary=b_dataset_format_dictionary,
            )

    return b_dataset_format_dictionary
