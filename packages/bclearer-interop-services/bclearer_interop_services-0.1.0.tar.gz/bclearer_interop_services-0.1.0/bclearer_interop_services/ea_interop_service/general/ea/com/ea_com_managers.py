from bclearer_interop_services.file_system_service.file_selector import (
    select_file,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


class EaComManagers:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass

    @staticmethod
    def get_ea_repository_file() -> (
        Files
    ):
        file = select_file()

        return file
