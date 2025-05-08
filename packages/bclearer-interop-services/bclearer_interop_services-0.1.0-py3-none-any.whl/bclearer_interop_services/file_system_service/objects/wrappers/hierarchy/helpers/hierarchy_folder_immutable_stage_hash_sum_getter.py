from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def get_hierarchy_folder_immutable_stage_hash_sum(
    hierarchy_file_system_object_universe_register,
    hierarchy_folder: HierarchyFolders,
    hierarchy_folder_immutable_stage_hash_sum: int,
) -> int:
    from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
        HierarchyFileSystemObjectRegisters,
    )

    if not isinstance(
        hierarchy_file_system_object_universe_register,
        HierarchyFileSystemObjectRegisters,
    ):
        raise TypeError

    child_hierarchy_file_system_objects = (
        hierarchy_folder.child_hierarchy_file_system_objects
    )

    for child_hierarchy_file_system_object in child_hierarchy_file_system_objects:
        child_immutable_stage_content_hash = __get_child_immutable_stage_content_hash(
            hierarchy_file_system_object_universe_register=hierarchy_file_system_object_universe_register,
            child_hierarchy_file_system_object=child_hierarchy_file_system_object,
        )

        hierarchy_folder_immutable_stage_hash_sum += child_immutable_stage_content_hash

    hierarchy_folder.hierarchy_folder_immutable_stage_hash_sum = hierarchy_folder_immutable_stage_hash_sum

    return hierarchy_folder_immutable_stage_hash_sum


def __get_child_immutable_stage_content_hash(
    hierarchy_file_system_object_universe_register,
    child_hierarchy_file_system_object: HierarchyFileSystemObjects,
) -> int:
    child_file_system_object = hierarchy_file_system_object_universe_register.get_file_system_object_from_hierarchy_object(
        hierarchy_file_system_object=child_hierarchy_file_system_object,
    )

    if isinstance(
        child_file_system_object,
        Files,
    ):
        return (
            child_file_system_object.file_immutable_stage_hash
        )

    if isinstance(
        child_hierarchy_file_system_object,
        HierarchyFolders,
    ):
        hierarchy_folder_immutable_stage_content_hash_sum = get_hierarchy_folder_immutable_stage_hash_sum(
            hierarchy_file_system_object_universe_register=hierarchy_file_system_object_universe_register,
            hierarchy_folder=child_hierarchy_file_system_object,
            hierarchy_folder_immutable_stage_hash_sum=0,
        )

        return hierarchy_folder_immutable_stage_content_hash_sum

    raise TypeError
