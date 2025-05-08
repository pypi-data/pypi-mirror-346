from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


class EaRepositories:

    def __init__(
        self,
        short_name: str,
        ea_repository_file: Files = None,
    ):
        self.ea_repository_file = (
            ea_repository_file
        )

        self.short_name = short_name
