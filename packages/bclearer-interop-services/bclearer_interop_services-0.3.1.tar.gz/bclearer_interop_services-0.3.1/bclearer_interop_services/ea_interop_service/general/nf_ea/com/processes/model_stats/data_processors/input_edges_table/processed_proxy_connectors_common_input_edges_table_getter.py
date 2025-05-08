from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
    outer_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CLASSIFIER_COLUMN_NAME,
    NF_UUIDS2_COLUMN_NAME,
    UUID_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.dataframe_services.uuid_column_generator import (
    add_uuid_column_to_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.input_edges_table.input_edges_base_table_human_readable_fields_adder import (
    add_human_readable_fields_to_input_edges_base_table,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from pandas import DataFrame, concat


def get_processed_proxy_connectors_common_input_edges_table(
    ea_connectors: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    ea_connectors_only_new_broken_down_connectors = __get_new_broken_down_connectors_from_proxy_connectors(
        ea_connectors=ea_connectors,
        ea_classifiers=ea_classifiers,
    )

    ea_connectors_only_new_broken_down_connectors_uuidified = __add_uuids_to_new_connectors_dataframe(
        connectors_dataframe=ea_connectors_only_new_broken_down_connectors
    )

    ea_connectors_without_proxy_connectors = __remove_proxy_connectors_from_ea_connectors(
        ea_classifiers=ea_classifiers,
        ea_connectors=ea_connectors,
    )

    processed_proxy_connectors_common_input_edges_base_table = concat(
        [
            ea_connectors_only_new_broken_down_connectors_uuidified,
            ea_connectors_without_proxy_connectors,
        ]
    ).reset_index()

    processed_proxy_connectors_common_input_edges_base_table = processed_proxy_connectors_common_input_edges_base_table.filter(
        items=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            NfColumnTypes.NF_UUIDS.column_name,
        ]
    )

    processed_proxy_connectors_input_edges_human_readable_table = add_human_readable_fields_to_input_edges_base_table(
        input_edges_base_table=processed_proxy_connectors_common_input_edges_base_table,
        ea_classifiers=ea_classifiers,
    )

    return processed_proxy_connectors_input_edges_human_readable_table


def __get_new_broken_down_connectors_from_proxy_connectors(
    ea_connectors: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    new_broken_down_connector_place_1_half_renaming_dictionary = {
        NF_UUIDS2_COLUMN_NAME: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
    }

    # Note: previously, the connector place names were inverted, this one was assigned to '_place_2'
    temporary_dataframe_with_supplier_place1_end_connector = __get_new_broken_down_connector_half(
        ea_connectors=ea_connectors,
        ea_classifiers=ea_classifiers,
        renaming_dictionary=new_broken_down_connector_place_1_half_renaming_dictionary,
        connector_place="_place_1",
    )

    new_broken_down_connector_place_2_half_renaming_dictionary = {
        NF_UUIDS2_COLUMN_NAME: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
    }

    # Note: previously, the connector place names were inverted, this one was assigned to '_place_1'
    temporary_dataframe_with_client_place2_end_connector = __get_new_broken_down_connector_half(
        ea_connectors=ea_connectors,
        ea_classifiers=ea_classifiers,
        renaming_dictionary=new_broken_down_connector_place_2_half_renaming_dictionary,
        connector_place="_place_2",
    )

    new_broken_down_connectors_from_proxy_connectors = concat(
        [
            temporary_dataframe_with_supplier_place1_end_connector,
            temporary_dataframe_with_client_place2_end_connector,
        ]
    ).reset_index(
        drop=True
    )

    return new_broken_down_connectors_from_proxy_connectors


def __add_uuids_to_new_connectors_dataframe(
    connectors_dataframe: DataFrame,
) -> DataFrame:
    uuidified_new_connectors_dataframe = add_uuid_column_to_dataframe(
        dataframe=connectors_dataframe,
        column=UUID_COLUMN_NAME,
    )

    return uuidified_new_connectors_dataframe


def __get_new_broken_down_connector_half(
    ea_connectors: DataFrame,
    ea_classifiers: DataFrame,
    renaming_dictionary: dict,
    connector_place: str,
) -> DataFrame:
    ea_classifiers_filtered_to_proxy_connectors = ea_classifiers.loc[
        ea_classifiers[
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
        ].isin(
            [
                EaElementTypes.PROXY_CONNECTOR.type_name
            ]
        )
    ]

    ea_classifiers_columns = {
        UUID_COLUMN_NAME: UUID_COLUMN_NAME
    }

    temporary_dataframe = inner_merge_dataframes(
        master_dataframe=ea_connectors,
        master_dataframe_key_columns=[
            UUID_COLUMN_NAME
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers_filtered_to_proxy_connectors,
        foreign_key_dataframe_fk_columns=[
            CLASSIFIER_COLUMN_NAME
        ],
        foreign_key_dataframe_other_column_rename_dictionary=ea_classifiers_columns,
    )

    temporary_dataframe_filtered_and_renamed = dataframe_filter_and_rename(
        dataframe=temporary_dataframe,
        filter_and_rename_dictionary=renaming_dictionary,
    )

    new_connectors_dataframe = __add_connector_type_name_to_new_connectors(
        new_connectors_dataframe=temporary_dataframe_filtered_and_renamed,
        connector_place=connector_place,
    )

    return new_connectors_dataframe


def __add_connector_type_name_to_new_connectors(
    new_connectors_dataframe: DataFrame,
    connector_place: str,
) -> DataFrame:

    connection_type_list = new_connectors_dataframe[
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
    ].to_list()

    for (
        connector_type
    ) in new_connectors_dataframe[
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
    ]:
        if (
            connector_type
            in connection_type_list
        ):
            new_connectors_dataframe[
                NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
            ] = (
                connector_type
                + connector_place
            )

    return new_connectors_dataframe


def __remove_proxy_connectors_from_ea_connectors(
    ea_classifiers: DataFrame,
    ea_connectors: DataFrame,
) -> DataFrame:
    ea_classifiers_filtered_to_proxy_connectors = ea_classifiers.loc[
        ea_classifiers[
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
        ].isin(
            [
                EaElementTypes.PROXY_CONNECTOR.type_name
            ]
        )
    ]

    ea_classifiers_proxy_connector_columns = {
        UUID_COLUMN_NAME: UUID_COLUMN_NAME
    }

    temporary_dataframe_no_proxy_connectors = outer_merge_dataframes(
        master_dataframe=ea_connectors,
        master_dataframe_key_columns=[
            UUID_COLUMN_NAME
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers_filtered_to_proxy_connectors,
        foreign_key_dataframe_fk_columns=[
            CLASSIFIER_COLUMN_NAME
        ],
        foreign_key_dataframe_other_column_rename_dictionary=ea_classifiers_proxy_connector_columns,
    )

    temporary_dataframe_no_proxy_connectors_filtered = temporary_dataframe_no_proxy_connectors[
        temporary_dataframe_no_proxy_connectors[
            UUID_COLUMN_NAME + "2"
        ].isnull()
    ].reset_index()

    temporary_ea_connectors_dataframe_columns = {
        UUID_COLUMN_NAME
        + "1": UUID_COLUMN_NAME,
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
    }

    temporary_ea_connectors_dataframe = dataframe_filter_and_rename(
        dataframe=temporary_dataframe_no_proxy_connectors_filtered,
        filter_and_rename_dictionary=temporary_ea_connectors_dataframe_columns,
    ).drop_duplicates()

    clean_ea_connectors_dataframe = temporary_ea_connectors_dataframe[
        temporary_ea_connectors_dataframe[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        ].notnull()
    ].reset_index(
        drop=True
    )

    return clean_ea_connectors_dataframe
