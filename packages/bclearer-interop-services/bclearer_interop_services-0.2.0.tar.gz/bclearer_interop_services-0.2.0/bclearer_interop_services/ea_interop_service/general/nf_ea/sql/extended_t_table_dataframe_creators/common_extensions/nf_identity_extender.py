from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame


def extend_with_identities(
    dataframe: DataFrame,
    universe_key: str,
    collection_type_name: str,
) -> DataFrame:
    extended_dataframe = (
        dataframe.copy()
    )

    universe_keys_column_name = (
        NfColumnTypes.UNIVERSE_KEYS.column_name
    )

    extended_dataframe[
        universe_keys_column_name
    ] = universe_key

    collection_types_column_name = (
        NfColumnTypes.COLLECTION_TYPES.column_name
    )

    extended_dataframe[
        collection_types_column_name
    ] = collection_type_name

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    extended_dataframe[
        nf_uuids_column_name
    ] = extended_dataframe.apply(
        lambda row: create_new_uuid(),
        axis=1,
    )

    return extended_dataframe
