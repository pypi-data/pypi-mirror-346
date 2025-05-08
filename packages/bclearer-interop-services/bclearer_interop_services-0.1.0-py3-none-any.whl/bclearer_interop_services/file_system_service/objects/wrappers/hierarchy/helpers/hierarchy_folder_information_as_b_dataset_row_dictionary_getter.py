from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def get_hierarchy_folder_information_as_b_dataset_row_dictionary(
    hierarchy_file_system_object_register,
    hierarchy_folder: HierarchyFolders,
) -> dict:
    from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
        HierarchyFileSystemObjectRegisters,
    )

    if not isinstance(
        hierarchy_file_system_object_register,
        HierarchyFileSystemObjectRegisters,
    ):
        raise TypeError

    folder = hierarchy_file_system_object_register.get_file_system_object_from_hierarchy_object(
        hierarchy_file_system_object=hierarchy_folder,
    )

    if (
        not hierarchy_folder.parent_hierarchy_folder
    ):
        parent_uuid = ""

    else:
        parent_uuid = (
            hierarchy_folder.parent_hierarchy_folder.uuid
        )

    hierarchy_folder_as_b_dataset_row_dictionary = {
        "uuid": hierarchy_folder.uuid,
        "hierarchy_file_system_object_type": type(
            hierarchy_folder,
        ).__name__,
        "child_count": str(
            hierarchy_folder.get_child_hierarchy_object_count(),
        ),
        "full_name": folder.absolute_path_string,
        "base_name": folder.base_name,
        "hierarchy_folder_immutable_stage_hash_sum": hierarchy_folder.hierarchy_folder_immutable_stage_hash_sum,
        "length": str(
            folder.file_system_object_properties.length,
        ),
        "extension": folder.file_system_object_properties.extension,
        "creation_time": folder.file_system_object_properties.creation_time,
        "last_access_time": folder.file_system_object_properties.last_access_time,
        "last_write_time": folder.file_system_object_properties.last_write_time,
        "parent_uuid": parent_uuid,
        "relative_path": hierarchy_folder.relative_path,
    }

    return hierarchy_folder_as_b_dataset_row_dictionary
