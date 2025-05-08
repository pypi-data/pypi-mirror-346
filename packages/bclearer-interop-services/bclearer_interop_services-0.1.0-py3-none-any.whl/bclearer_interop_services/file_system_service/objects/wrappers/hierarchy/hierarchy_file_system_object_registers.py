import os.path

from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_dataset_register_into_access_exporter import (
    export_b_dataset_register_into_access,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_dataset_register_into_sqlite_exporter import (
    export_register_into_sqlite,
)
from bclearer_interop_services.file_system_service.first_level_deep_file_system_objects_getter import (
    get_first_level_children_file_system_object_paths,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.child_path_to_hierarchy_adder import (
    add_child_path_to_hierarchy,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.hierarchy_folder_immutable_stage_hash_sum_getter import (
    get_hierarchy_folder_immutable_stage_hash_sum,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.hierarchy_folder_to_b_dataset_format_adder import (
    add_hierarchy_folder_to_b_dataset_format,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)
from nf_common.code.services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


class HierarchyFileSystemObjectRegisters:
    def __init__(
        self,
        owning_object: object,
        root_file_system_object: FileSystemObjects,
        root_hierarchy_folder: HierarchyFolders,
    ):
        self.owning_object = (
            owning_object
        )

        self.root = (
            root_hierarchy_folder
        )

        self.hierarchy_objects_to_file_system_objects_mapping = (
            dict()
        )

        self.add_hierarchy_object_to_file_system_object_map_to_register(
            hierarchy_file_system_object=root_hierarchy_folder,
            file_system_object=root_file_system_object,
        )

        self.__add_hierarchy_to_root()

        self.__populate_folder_lengths_in_bytes()

        self.__populate_hierarchy_folders_immutable_stage_hash_sums(
            hierarchy_folder=self.root,
            hierarchy_folder_immutable_stage_hash_sum=0,
        )

    @run_and_log_function
    def __populate_hierarchy_folders_immutable_stage_hash_sums(
        self,
        hierarchy_folder: HierarchyFolders,
        hierarchy_folder_immutable_stage_hash_sum: int,
    ) -> None:
        hierarchy_folder_immutable_stage_hash_sum = get_hierarchy_folder_immutable_stage_hash_sum(
            hierarchy_file_system_object_universe_register=self,
            hierarchy_folder=hierarchy_folder,
            hierarchy_folder_immutable_stage_hash_sum=hierarchy_folder_immutable_stage_hash_sum,
        )

        hierarchy_folder.b_identity_component_immutable_stage_sum = hierarchy_folder_immutable_stage_hash_sum

    @run_and_log_function
    def __add_hierarchy_to_root(
        self,
    ) -> None:
        self.add_hierarchy_folder_to_hierarchy(
            hierarchy_folder=self.root,
        )

    def add_hierarchy_folder_to_hierarchy(
        self,
        hierarchy_folder: HierarchyFolders,
    ) -> None:
        folder = self.get_file_system_object_from_hierarchy_object(
            hierarchy_file_system_object=hierarchy_folder,
        )

        first_level_children_paths = get_first_level_children_file_system_object_paths(
            input_file_system_object=folder,
            extension_to_filter="",
        )

        for (
            child_path
        ) in first_level_children_paths:
            add_child_path_to_hierarchy(
                hierarchy_file_system_object_register=self,
                child_path=child_path,
                parent_hierarchy_folder=hierarchy_folder,
            )

    def add_hierarchy_object_to_file_system_object_map_to_register(
        self,
        hierarchy_file_system_object: HierarchyFileSystemObjects,
        file_system_object: FileSystemObjects,
    ) -> None:
        self.hierarchy_objects_to_file_system_objects_mapping[
            hierarchy_file_system_object
        ] = file_system_object

    def get_file_system_object_from_hierarchy_object(
        self,
        hierarchy_file_system_object: HierarchyFileSystemObjects,
    ) -> FileSystemObjects:
        file_system_object = self.hierarchy_objects_to_file_system_objects_mapping[
            hierarchy_file_system_object
        ]

        return file_system_object

    def get_hierarchy_object_from_file_system_object(
        self,
        input_file_system_object: FileSystemObjects,
    ) -> [
        HierarchyFolders,
        HierarchyFileSystemObjects,
    ]:
        for (
            hierarchy_file_system_object,
            file_system_object,
        ) in (
            self.hierarchy_objects_to_file_system_objects_mapping.items()
        ):
            if (
                input_file_system_object
                == file_system_object
            ):
                return hierarchy_file_system_object

    @run_and_log_function
    def __populate_folder_lengths_in_bytes(
        self,
    ) -> None:
        for (
            hierarchy_file_system_object,
            file_system_object,
        ) in (
            self.hierarchy_objects_to_file_system_objects_mapping.items()
        ):
            if isinstance(
                file_system_object,
                Folders,
            ):
                file_system_object.populate_folder_length_in_bytes()

    def export_register_in_b_datasets_format(
        self,
    ) -> dict:
        hierarchy_file_system_object_register_in_b_datasets_format = (
            dict()
        )

        if isinstance(
            self.root,
            HierarchyFolders,
        ):
            add_hierarchy_folder_to_b_dataset_format(
                hierarchy_file_system_object_register=self,
                hierarchy_folder=self.root,
                b_dataset_format_dictionary=hierarchy_file_system_object_register_in_b_datasets_format,
            )

        else:
            raise TypeError

        return hierarchy_file_system_object_register_in_b_datasets_format

    def get_relative_path(
        self,
        hierarchy_file_system_object: HierarchyFileSystemObjects,
    ) -> str:
        root_path = self.get_file_system_object_from_hierarchy_object(
            hierarchy_file_system_object=self.root,
        ).absolute_path_string

        relative_path = os.path.relpath(
            path=self.get_file_system_object_from_hierarchy_object(
                hierarchy_file_system_object=hierarchy_file_system_object,
            ).absolute_path_string,
            start=root_path,
        )

        return relative_path

    def export_register_into_access(
        self,
        output_folder: Folders,
        register_in_b_datasets_format: dict = None,
    ) -> None:
        export_b_dataset_register_into_access(
            register_object=self,
            output_folder=output_folder,
            register_output_string_name_root="hierarchy_file_system_objects",
            register_in_b_datasets_format=register_in_b_datasets_format,
        )

    def export_register_into_sqlite(
        self,
        output_folder: Folders,
        register_in_b_datasets_format: dict = None,
    ) -> None:
        export_register_into_sqlite(
            register_object=self,
            output_folder=output_folder,
            register_output_string_name_root="hierarchy_file_system_objects",
            register_in_b_datasets_format=register_in_b_datasets_format,
        )
