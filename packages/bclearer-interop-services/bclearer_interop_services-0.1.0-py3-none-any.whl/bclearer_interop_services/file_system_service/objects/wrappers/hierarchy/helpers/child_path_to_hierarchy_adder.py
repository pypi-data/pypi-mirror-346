import os

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def add_child_path_to_hierarchy(
    hierarchy_file_system_object_register,
    child_path: str,
    parent_hierarchy_folder: HierarchyFolders,
) -> None:
    from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
        HierarchyFileSystemObjectRegisters,
    )

    if not isinstance(
        hierarchy_file_system_object_register,
        HierarchyFileSystemObjectRegisters,
    ):
        raise TypeError

    if os.path.isfile(child_path):
        __add_child_file_path_to_hierarchy(
            child_path=child_path,
            parent_hierarchy_folder=parent_hierarchy_folder,
            hierarchy_file_system_object_register=hierarchy_file_system_object_register,
        )

    if os.path.isdir(child_path):
        __add_child_folder_path_to_hierarchy(
            child_path=child_path,
            parent_hierarchy_folder=parent_hierarchy_folder,
            hierarchy_file_system_object_register=hierarchy_file_system_object_register,
        )


def __add_child_file_path_to_hierarchy(
    child_path: str,
    parent_hierarchy_folder: HierarchyFolders,
    hierarchy_file_system_object_register,
) -> None:
    child_file = Files(
        absolute_path_string=child_path,
    )

    child_hierarchy_file = HierarchyFileSystemObjects(
        file_system_object=child_file,
        parent_hierarchy_folder=parent_hierarchy_folder,
    )

    hierarchy_file_system_object_register.add_hierarchy_object_to_file_system_object_map_to_register(
        hierarchy_file_system_object=child_hierarchy_file,
        file_system_object=child_file,
    )

    child_hierarchy_file.relative_path = hierarchy_file_system_object_register.get_relative_path(
        hierarchy_file_system_object=child_hierarchy_file,
    )


def __add_child_folder_path_to_hierarchy(
    child_path: str,
    parent_hierarchy_folder: HierarchyFolders,
    hierarchy_file_system_object_register,
) -> None:
    child_folder = Folders(
        absolute_path_string=child_path,
    )

    child_hierarchy_folder = HierarchyFolders(
        folder=child_folder,
        parent_hierarchy_folder=parent_hierarchy_folder,
    )

    hierarchy_file_system_object_register.add_hierarchy_object_to_file_system_object_map_to_register(
        hierarchy_file_system_object=child_hierarchy_folder,
        file_system_object=child_folder,
    )

    child_hierarchy_folder.relative_path = hierarchy_file_system_object_register.get_relative_path(
        hierarchy_file_system_object=child_hierarchy_folder,
    )

    hierarchy_file_system_object_register.add_hierarchy_folder_to_hierarchy(
        hierarchy_folder=child_hierarchy_folder,
    )
