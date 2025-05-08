import os
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


class Folders(FileSystemObjects):
    def __init__(
        self,
        absolute_path_string: str,
        parent_folder: object = None,
    ):
        super().__init__(
            absolute_path_string=absolute_path_string,
        )

        if (
            parent_folder
            and not isinstance(
                parent_folder,
                Folders,
            )
        ):
            raise TypeError

        self.child_folders = set()

        self.child_files = set()

        self.__add_to_parent(
            parent_folder=parent_folder,
        )

    def add_to_child_folders(
        self,
        child_file_system_object: "Folders",
    ):
        self.child_folders.add(
            child_file_system_object,
        )

    def add_to_child_files(
        self,
        child_file_system_object: Files,
    ):
        self.child_files.add(
            child_file_system_object,
        )

    def __add_to_parent(
        self,
        parent_folder: "Folders",
    ):
        if parent_folder is None:
            return

        parent_folder.add_to_child_folders(
            self,
        )

    def get_file_count(self) -> int:
        return len(self.child_files)

    def get_folder_count(self) -> int:
        return len(self.child_folders)

    def populate_folder_length_in_bytes(
        self,
    ) -> None:
        descendants_list = list(
            Path(
                self.absolute_path_string,
            ).rglob("*"),
        )

        file_descendant_lengths = list()

        for (
            descendant_path
        ) in descendants_list:
            if os.path.isfile(
                descendant_path,
            ):
                file_descendant_lengths.append(
                    os.path.getsize(
                        descendant_path,
                    ),
                )

        self.file_system_object_properties.length = sum(
            file_descendant_lengths,
        )

    # TODO: The two following methods should be moved to the corresponding Hierarchy objects -  - Consider deprecation
    #  or keep it for flat File system object output
    def add_folder_to_b_dataset_format(
        self,
        b_dataset_format_dictionary: dict,
    ) -> dict:
        b_dataset_format_dictionary[
            self.uuid
        ] = (
            self.get_folder_information_as_b_dataset_row_dictionary()
        )

        for (
            child_file
        ) in self.child_files:
            b_dataset_format_dictionary[
                child_file.uuid
            ] = (
                child_file.get_file_as_b_dataset_row_dictionary()
            )

        for (
            child_folder
        ) in self.child_folders:
            child_folder.add_folder_to_b_dataset_format(
                b_dataset_format_dictionary=b_dataset_format_dictionary,
            )

        return (
            b_dataset_format_dictionary
        )

    def get_folder_information_as_b_dataset_row_dictionary(
        self,
    ) -> dict:
        if not self.parent_folder:
            parent_uuid = ""

            relative_path = ""

        else:
            parent_uuid = (
                self.parent_folder.uuid
            )

            relative_path = self.absolute_path_string.replace(
                self.parent_folder.absolute_path_string,
                "",
            )

        folder_as_b_dataset_row_dictionary = {
            "uuid": self.uuid,
            "file_system_object_type": type(
                self,
            ).__name__,
            "file_count": str(
                self.get_file_count(),
            ),
            "folder_count": str(
                self.get_folder_count(),
            ),
            "full_name": self.absolute_path_string,
            "base_name": self.base_name,
            "length": str(
                self.file_system_object_properties.length,
            ),
            "extension": self.file_system_object_properties.extension,
            "creation_time": self.file_system_object_properties.creation_time,
            "last_access_time": self.file_system_object_properties.last_access_time,
            "last_write_time": self.file_system_object_properties.last_write_time,
            "parent_uuid": parent_uuid,
            "relative_path": relative_path,
        }

        return folder_as_b_dataset_row_dictionary
