from bclearer_interop_services.file_system_service.bie_file_system_domain.common_knowledge.file_system_b_identity_types import (
    FileSystemBIdentityTypes,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_sum_from_strings_creator import (
    create_b_identity_sum_from_strings,
)


class BIdentityFileSystemObjects:
    def __init__(
        self,
        file_system_object: FileSystemObjects,
    ):
        # TODO: Temporary bIdentity given - to be discussed
        self.id_b_identity = create_b_identity_sum_from_strings(
            strings=[
                FileSystemBIdentityTypes.B_IDENTITY_FILE_SYSTEM_OBJECTS.b_identity_name,
                file_system_object.absolute_path_string,
            ],
        )
