from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)


class HierarchyFolders(
    HierarchyFileSystemObjects,
):
    def __init__(
        self,
        folder: Folders,
        parent_hierarchy_folder: object = None,
    ):
        super().__init__(
            file_system_object=folder,
            parent_hierarchy_folder=parent_hierarchy_folder,
        )

        self.child_hierarchy_file_system_objects = (
            set()
        )

        self.hierarchy_folder_immutable_stage_hash_sum = (
            0
        )

    # TODO: To be deprecated? - Is not being used
    # def add_child_hierarchy_file_system_object(
    #         self,
    #         child_hierarchy_file_system_object: HierarchyFileSystemObjects) \
    #         -> None:
    #     if not isinstance(child_hierarchy_file_system_object, HierarchyFileSystemObjects):
    #         raise \
    #             TypeError
    #
    #     self.child_hierarchy_file_system_objects.add(
    #         child_hierarchy_file_system_object)

    def get_child_hierarchy_object_count(
        self,
    ) -> int:
        return len(
            self.child_hierarchy_file_system_objects,
        )
