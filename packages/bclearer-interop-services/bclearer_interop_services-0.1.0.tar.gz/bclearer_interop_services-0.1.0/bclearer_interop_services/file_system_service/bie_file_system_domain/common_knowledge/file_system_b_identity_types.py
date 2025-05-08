from enum import Enum, auto


class FileSystemBIdentityTypes(Enum):
    NOT_SET = auto()

    B_IDENTITY_FILE_SYSTEM_OBJECTS = (
        auto()
    )

    B_IDENTITY_FOLDERS = auto()

    B_IDENTITY_FILES = auto()

    def __b_identity_type_name(
        self,
    ) -> str:
        b_identity_type_name = (
            app_type_to_name_mapping[
                self
            ]
        )

        return b_identity_type_name

    b_identity_name = property(
        fget=__b_identity_type_name,
    )


app_type_to_name_mapping = {
    FileSystemBIdentityTypes.NOT_SET: "",
    FileSystemBIdentityTypes.B_IDENTITY_FILE_SYSTEM_OBJECTS: "b_identity_file_system_objects",
    FileSystemBIdentityTypes.B_IDENTITY_FOLDERS: "b_identity_folders",
    FileSystemBIdentityTypes.B_IDENTITY_FILES: "b_identity_files",
}
