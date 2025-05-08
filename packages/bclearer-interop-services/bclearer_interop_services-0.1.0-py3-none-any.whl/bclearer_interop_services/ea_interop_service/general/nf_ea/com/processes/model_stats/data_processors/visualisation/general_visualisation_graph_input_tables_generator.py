from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME,
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME,
)
from pandas import DataFrame


def generate_general_visualisation_graph_input_tables(
    ea_connectors: DataFrame,
) -> DataFrame:
    general_edges_dataframe = ea_connectors.filter(
        items=[
            SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME,
            CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME,
            EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
        ]
    )
    return general_edges_dataframe
