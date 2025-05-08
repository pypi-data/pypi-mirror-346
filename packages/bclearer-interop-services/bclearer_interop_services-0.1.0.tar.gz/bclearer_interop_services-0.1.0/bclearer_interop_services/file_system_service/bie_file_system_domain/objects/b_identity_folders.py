from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_objects import (
    BIdentityFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class BIdentityFolders(
    BIdentityFileSystemObjects,
):
    def __init__(self, folder: Folders):
        super().__init__(
            file_system_object=folder,
        )

        self.b_identity_component_immutable_stage_sum = (
            0
        )

        self.id_b_identity_component_id_sum = (
            0
        )
