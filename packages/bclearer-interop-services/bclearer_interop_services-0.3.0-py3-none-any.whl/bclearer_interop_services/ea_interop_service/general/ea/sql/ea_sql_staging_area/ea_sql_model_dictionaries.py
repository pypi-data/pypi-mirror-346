from typing import Dict

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class EaSqlModelDictionaries:
    def __init__(self):
        self.ea_sql_model_dictionary = (
            Dict[
                EaCollectionTypes,
                DataFrame,
            ]
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass
