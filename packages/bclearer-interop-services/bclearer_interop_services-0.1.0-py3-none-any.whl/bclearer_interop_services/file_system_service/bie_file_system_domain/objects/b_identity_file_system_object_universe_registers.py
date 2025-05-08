from typing import Optional

from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_objects import (
    BIdentityFileSystemObjects,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_folders import (
    BIdentityFolders,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_dataset_register_into_access_exporter import (
    export_b_dataset_register_into_access,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_dataset_register_into_sqlite_exporter import (
    export_register_into_sqlite,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_identity_columns_to_register_in_b_dataset_format_adder import (
    add_b_identity_columns_to_register_in_b_dataset_format,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_identity_folder_id_b_identity_component_id_sum_getter import (
    get_b_identity_folder_id_b_identity_component_id_sum,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.helpers.b_identity_to_hierarchy_register_map_entry_to_dictionary_adder import (
    add_b_identity_to_hierarchy_register_map_entry_to_dictionary,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_object_registers import (
    HierarchyFileSystemObjectRegisters,
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


class BIdentityFileSystemObjectUniverseRegisters:
    def __init__(
        self,
        owning_b_identity_file_system_object_universe,
        root_file_system_object: FileSystemObjects,
        root_b_identity_folder: BIdentityFolders,
    ):
        from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universes import (
            BIdentityFileSystemObjectUniverses,
        )

        if not isinstance(
            owning_b_identity_file_system_object_universe,
            BIdentityFileSystemObjectUniverses,
        ):
            raise TypeError

        self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping = (
            dict()
        )

        self.owning_universe = owning_b_identity_file_system_object_universe

        self.root = (
            root_b_identity_folder
        )

        if not isinstance(
            root_file_system_object,
            Folders,
        ):
            raise TypeError

        root_hierarchy_folder = HierarchyFolders(
            folder=root_file_system_object,
        )

        self.hierarchy_file_system_object_register = HierarchyFileSystemObjectRegisters(
            owning_object=self,
            root_file_system_object=root_file_system_object,
            root_hierarchy_folder=root_hierarchy_folder,
        )

        self.root.b_identity_component_immutable_stage_sum = (
            root_hierarchy_folder.hierarchy_folder_immutable_stage_hash_sum
        )

        self.add_b_identity_file_system_object_to_hierarchy_file_system_objects_map_to_register(
            b_identity_file_system_object=root_b_identity_folder,
            hierarchy_file_system_object=root_hierarchy_folder,
        )

        self.__populate_mapping_dictionary()

        self.__populate_id_b_identity_component_id_sums()

    @run_and_log_function
    def __populate_mapping_dictionary(
        self,
    ) -> None:
        hierarchy_file_system_object_mapping_dictionary = (
            self.hierarchy_file_system_object_register.hierarchy_objects_to_file_system_objects_mapping
        )

        for (
            hierarchy_file_system_object,
            file_system_object,
        ) in (
            hierarchy_file_system_object_mapping_dictionary.items()
        ):
            add_b_identity_to_hierarchy_register_map_entry_to_dictionary(
                b_identity_file_system_object_universe_register=self,
                hierarchy_file_system_object=hierarchy_file_system_object,
                file_system_object=file_system_object,
            )

    @run_and_log_function
    def __populate_id_b_identity_component_id_sums(
        self,
    ) -> None:
        for (
            b_identity_file_system_object,
            hierarchy_file_system_object,
        ) in (
            self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping.items()
        ):
            if isinstance(
                b_identity_file_system_object,
                BIdentityFolders,
            ):
                b_identity_folder_id_b_identity_component_id_sum = get_b_identity_folder_id_b_identity_component_id_sum(
                    b_identity_file_system_object_registry=self,
                    hierarchy_folder=hierarchy_file_system_object,
                )

                b_identity_file_system_object.id_b_identity_component_id_sum = b_identity_folder_id_b_identity_component_id_sum

    def add_b_identity_file_system_object_to_hierarchy_file_system_objects_map_to_register(
        self,
        b_identity_file_system_object: BIdentityFileSystemObjects,
        hierarchy_file_system_object: HierarchyFileSystemObjects,
    ) -> None:
        self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping[
            b_identity_file_system_object
        ] = hierarchy_file_system_object

    def get_identity_b_identity_file_system_object_from_hierarchy_object(
        self,
        hierarchy_file_system_object,
    ) -> (
        BIdentityFileSystemObjects
        | None
    ):
        # TODO: This is being done using list comprehension, it maybe more BOROish with the for loop deployed
        identity_b_identity_file_system_objects = [
            identity_b_identity_file_system_object
            for identity_b_identity_file_system_object, current_hierarchy_file_system_object in self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping.items()
            if current_hierarchy_file_system_object
            == hierarchy_file_system_object
        ]

        if identity_b_identity_file_system_objects:
            return identity_b_identity_file_system_objects[
                0
            ]

        return None

    def get_identity_hierarchy_file_system_object_from_b_identity_object(
        self,
        b_identity_file_system_object,
    ) -> HierarchyFileSystemObjects:
        identity_hierarchy_file_system_object = self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping[
            b_identity_file_system_object
        ]

        return identity_hierarchy_file_system_object

    def get_hierarchy_file_system_object_by_uuid(
        self,
        hierarchy_file_system_object_uuid: str,
    ) -> (
        HierarchyFileSystemObjects
        | None
    ):
        for (
            hierarchy_file_system_object
        ) in (
            self.b_identity_file_system_objects_to_hierarchy_file_system_objects_mapping.values()
        ):
            if (
                hierarchy_file_system_object_uuid
                == hierarchy_file_system_object.uuid
            ):
                return hierarchy_file_system_object

        return None

    def export_register_in_b_datasets_format(
        self,
    ) -> dict:
        hierarchy_file_system_object_register_in_b_datasets_format = (
            self.hierarchy_file_system_object_register.export_register_in_b_datasets_format()
        )

        register_in_b_datasets_format = (
            dict()
        )

        for (
            hierarchy_file_system_object_register_in_b_datasets_format_uuid,
            hierarchy_file_system_object_register_in_b_datasets_format_row_dictionary,
        ) in (
            hierarchy_file_system_object_register_in_b_datasets_format.items()
        ):
            add_b_identity_columns_to_register_in_b_dataset_format(
                b_identity_file_system_object_universe_register=self,
                register_in_b_datasets_format=register_in_b_datasets_format,
                hierarchy_file_system_object_row_dictionary=hierarchy_file_system_object_register_in_b_datasets_format_row_dictionary,
                hierarchy_file_system_object_uuid=hierarchy_file_system_object_register_in_b_datasets_format_uuid,
            )

        return register_in_b_datasets_format

    # TODO: separate export to CSV from export to Access
    def export_register_into_access(
        self,
        output_folder: Folders,
        register_in_b_datasets_format: dict = None,
    ) -> None:
        export_b_dataset_register_into_access(
            register_object=self,
            output_folder=output_folder,
            register_output_string_name_root="b_identity_file_system_objects",
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
            register_output_string_name_root="b_identity_file_system_objects",
            register_in_b_datasets_format=register_in_b_datasets_format,
        )
