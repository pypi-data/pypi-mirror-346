from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


class HierarchyFileSystemObjects:
    def __init__(
        self,
        file_system_object: FileSystemObjects,
        parent_hierarchy_folder: object = None,
    ):
        # TODO: Note - property only created to aid the debugging - could be transformed or removed in the future
        self.name = (
            file_system_object.base_name
        )

        self.uuid = create_new_uuid()

        from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
            HierarchyFolders,
        )

        if (
            parent_hierarchy_folder
            and not isinstance(
                parent_hierarchy_folder,
                HierarchyFolders,
            )
        ):
            raise TypeError

        self.parent_hierarchy_folder = (
            parent_hierarchy_folder
        )

        self.relative_path = ""

        self.__add_to_parent_hierarchy_folder()

    def __add_to_parent_hierarchy_folder(
        self,
    ) -> None:
        if (
            not self.parent_hierarchy_folder
        ):
            return

        self.parent_hierarchy_folder.child_hierarchy_file_system_objects.add(
            self,
        )
