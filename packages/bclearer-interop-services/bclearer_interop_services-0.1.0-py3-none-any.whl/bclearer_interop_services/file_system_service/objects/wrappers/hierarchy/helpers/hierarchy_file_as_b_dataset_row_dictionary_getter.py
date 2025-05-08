from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)


def get_hierarchy_file_as_b_dataset_row_dictionary(
    hierarchy_file_system_object_register,
    hierarchy_file: HierarchyFileSystemObjects,
) -> dict:
    from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
        HierarchyFileSystemObjectRegisters,
    )

    if not isinstance(
        hierarchy_file_system_object_register,
        HierarchyFileSystemObjectRegisters,
    ):
        raise TypeError

    file = hierarchy_file_system_object_register.get_file_system_object_from_hierarchy_object(
        hierarchy_file_system_object=hierarchy_file,
    )

    hierarchy_file_as_b_dataset_row_dictionary = {
        "uuid": hierarchy_file.uuid,
        "hierarchy_file_system_object_type": type(
            hierarchy_file,
        ).__name__,
        "full_name": file.absolute_path_string,
        "base_name": file.base_name,
        "file_immutable_stage_hash": file.file_immutable_stage_hash,
        "length": str(
            file.file_system_object_properties.length,
        ),
        "extension": file.file_system_object_properties.extension,
        "creation_time": file.file_system_object_properties.creation_time,
        "last_access_time": file.file_system_object_properties.last_access_time,
        "last_write_time": file.file_system_object_properties.last_write_time,
        "parent_uuid": hierarchy_file.parent_hierarchy_folder.uuid,
        "relative_path": hierarchy_file.relative_path,
    }

    return hierarchy_file_as_b_dataset_row_dictionary
