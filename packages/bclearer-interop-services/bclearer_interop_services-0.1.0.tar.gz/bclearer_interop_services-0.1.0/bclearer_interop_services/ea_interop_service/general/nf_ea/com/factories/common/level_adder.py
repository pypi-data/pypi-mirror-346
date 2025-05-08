from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from pandas import DataFrame


def add_level(
    dataframe: DataFrame,
    next_level_dataframe: DataFrame,
):
    thin_ea_elements_columns = list(
        next_level_dataframe.columns
    )

    foreign_key_dataframe_other_column_rename_dictionary = (
        dict()
    )

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    for (
        thin_ea_elements_column
    ) in thin_ea_elements_columns:
        if (
            thin_ea_elements_column
            != nf_uuids_column_name
        ):
            foreign_key_dataframe_other_column_rename_dictionary[
                thin_ea_elements_column
            ] = thin_ea_elements_column

    dataframe = left_merge_dataframes(
        master_dataframe=dataframe,
        master_dataframe_key_columns=[
            nf_uuids_column_name
        ],
        merge_suffixes=[
            "_this_level",
            "_next_level",
        ],
        foreign_key_dataframe=next_level_dataframe,
        foreign_key_dataframe_fk_columns=[
            nf_uuids_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary=foreign_key_dataframe_other_column_rename_dictionary,
    )

    return dataframe
