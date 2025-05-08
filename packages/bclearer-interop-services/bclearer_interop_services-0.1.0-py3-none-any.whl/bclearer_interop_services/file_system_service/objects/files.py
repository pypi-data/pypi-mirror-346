from bclearer_interop_services.file_system_service.bie_file_system_domain.creators.file_b_identity_immutable_stage_base_creator import (
    create_file_b_identity_immutable_stage_base,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)


class Files(FileSystemObjects):
    def __init__(
        self,
        absolute_path_string: str,
        parent_folder: object = None,
    ):
        from bclearer_interop_services.file_system_service.objects.folders import (
            Folders,
        )

        if (
            parent_folder
            and not isinstance(
                parent_folder,
                Folders,
            )
        ):
            raise TypeError

        super().__init__(
            absolute_path_string=absolute_path_string,
        )

        self.file_immutable_stage_hash = create_file_b_identity_immutable_stage_base(
            file=self,
        )

        self.__add_to_parent(
            parent_folder=parent_folder,
        )

    def __add_to_parent(
        self,
        parent_folder: "Folders",
    ):
        if parent_folder is None:
            return

        self.parent_folder = (
            parent_folder
        )

        parent_folder.add_to_child_files(
            self,
        )

    # TODO: This method is being moved to the Hierarchy register - Consider deprecation or keep it for flat File system
    #  object output
    def get_file_as_b_dataset_row_dictionary(
        self,
    ) -> dict:
        relative_path = self.absolute_path_string.replace(
            self.parent_folder.absolute_path_string,
            "",
        )

        file_as_b_dataset_row_dictionary = {
            "uuid": self.uuid,
            "file_system_object_type": type(
                self,
            ).__name__,
            "full_name": self.absolute_path_string,
            "base_name": self.base_name,
            "length": str(
                self.file_system_object_properties.length,
            ),
            "extension": self.file_system_object_properties.extension,
            "file_immutable_stage_hash": self.file_immutable_stage_hash,
            "creation_time": self.file_system_object_properties.creation_time,
            "last_access_time": self.file_system_object_properties.last_access_time,
            "last_write_time": self.file_system_object_properties.last_write_time,
            "parent_uuid": self.parent_folder.uuid,
            "relative_path": relative_path,
        }

        return file_as_b_dataset_row_dictionary
