from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.input_edges_table.input_edges_base_table_human_readable_fields_adder import (
    add_human_readable_fields_to_input_edges_base_table,
)
from pandas import DataFrame


def get_common_input_edges_table(
    ea_classifiers: DataFrame,
    ea_connectors: DataFrame,
) -> DataFrame:
    common_input_edges_base_table = __get_common_input_edges_base_table(
        ea_connectors=ea_connectors
    )

    common_input_edges_human_readable_table = add_human_readable_fields_to_input_edges_base_table(
        input_edges_base_table=common_input_edges_base_table,
        ea_classifiers=ea_classifiers,
    )

    return common_input_edges_human_readable_table


def __get_common_input_edges_base_table(
    ea_connectors: DataFrame,
) -> DataFrame:
    common_input_edges_base_table = ea_connectors.filter(
        items=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            NfColumnTypes.NF_UUIDS.column_name,
        ]
    )

    return common_input_edges_base_table
