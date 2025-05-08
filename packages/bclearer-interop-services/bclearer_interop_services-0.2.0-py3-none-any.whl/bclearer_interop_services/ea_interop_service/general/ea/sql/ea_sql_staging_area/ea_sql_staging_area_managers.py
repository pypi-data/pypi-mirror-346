from typing import Dict

from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_staging_area.ea_sql_model_dictionaries import (
    EaSqlModelDictionaries,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)


class EaSqlStagingAreaManagers:
    def __init__(self):
        self.ea_repository_dictionary = Dict[
            EaRepositories,
            EaSqlModelDictionaries,
        ]

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass
