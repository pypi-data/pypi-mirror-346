from bclearer_interop_services.file_system_service.objects.wrappers.path_wrappers import (
    PathWrappers,
)


class AbsolutePathWrappers(
    PathWrappers,
):
    def __init__(
        self,
        absolute_path_string: str,
    ):
        super().__init__(
            absolute_path_string,
        )

    @property
    def absolute_path_string(
        self,
    ) -> str:
        absolute_path_string = (
            self.path_string
        )

        return absolute_path_string

    @property
    def absolute_level(self) -> int:
        absolute_level = self.level

        return absolute_level
