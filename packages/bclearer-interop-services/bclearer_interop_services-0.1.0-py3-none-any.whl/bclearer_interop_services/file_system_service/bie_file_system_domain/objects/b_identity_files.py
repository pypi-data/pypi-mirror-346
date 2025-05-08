from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_objects import (
    BIdentityFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


class BIdentityFiles(
    BIdentityFileSystemObjects,
):
    def __init__(self, file: Files):
        super().__init__(
            file_system_object=file,
        )

        self.b_identity_immutable_stage = (
            file.file_immutable_stage_hash
        )
