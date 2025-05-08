from typing import Optional

from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universe_registers import (
    BIdentityFileSystemObjectUniverseRegisters,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_folders import (
    BIdentityFolders,
)
from bclearer_interop_services.file_system_service.new_folder_creator import (
    create_new_folder,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


class BIdentityFileSystemObjectUniverses:
    def __init__(
        self,
        root_file_system_object: Folders,
    ):
        root_b_identity_folder = BIdentityFolders(
            folder=root_file_system_object,
        )

        self.b_identity_file_system_object_universe_registers = BIdentityFileSystemObjectUniverseRegisters(
            owning_b_identity_file_system_object_universe=self,
            root_file_system_object=root_file_system_object,
            root_b_identity_folder=root_b_identity_folder,
        )

        self.universe_output_root_folder: (
            Folders | None
        ) = None

    def export_universe_in_b_datasets_format(
        self,
    ) -> dict:
        universe_in_b_datasets_format = (
            self.b_identity_file_system_object_universe_registers.export_register_in_b_datasets_format()
        )

        return universe_in_b_datasets_format

    def get_universe_output_root_folder(
        self,
        universe_output_parent_folder: Folders,
    ) -> Folders:
        if (
            self.universe_output_root_folder
        ):
            return (
                self.universe_output_root_folder
            )

        universe_output_root_folder_path = create_new_folder(
            parent_folder_path=universe_output_parent_folder.absolute_path_string,
            new_folder_name="b_identity_fso_universe_"
            + now_time_as_string_for_files(),
        )

        self.universe_output_root_folder = Folders(
            absolute_path_string=universe_output_root_folder_path,
        )

        return (
            self.universe_output_root_folder
        )
