from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class CompressedFolders(Folders):
    def __init__(
        self,
        absolute_path_string: str,
    ):
        super().__init__(
            absolute_path_string=absolute_path_string,
        )
