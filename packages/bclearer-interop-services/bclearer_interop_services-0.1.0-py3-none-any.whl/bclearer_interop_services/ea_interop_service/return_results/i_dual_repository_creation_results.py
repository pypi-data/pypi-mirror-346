from bclearer_interop_services.ea_interop_service.i_dual_objects.i_repository import (
    IRepository,
)
from bclearer_interop_services.ea_interop_service.return_results.i_dual_repository_creation_result_types import (
    IDualRepositoryCreationResultTypes,
)


class IDualRepositoryCreationResults:

    def __init__(
        self,
        i_dual_repository: IRepository,
        i_dual_repository_creation_result_type: IDualRepositoryCreationResultTypes,
    ):
        self.i_dual_repository = (
            i_dual_repository
        )

        self.i_dual_repository_creation_result_type = i_dual_repository_creation_result_type

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass
