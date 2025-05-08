from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


class NullFiles(Files):
    def __init__(self):
        super().__init__(
            absolute_path_string="",
        )
