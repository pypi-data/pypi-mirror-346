from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    SOURCE_COLUMN_NAME,
    TARGET_COLUMN_NAME,
)
from networkx import (
    MultiDiGraph,
    is_empty,
)
from pandas import DataFrame


def get_edges_base_table_from_multi_edged_directed_graph(
    multi_edged_directed_graph: MultiDiGraph,
) -> DataFrame:
    if is_empty(
        multi_edged_directed_graph
    ):
        edges_base_table = DataFrame(
            columns=[
                SOURCE_COLUMN_NAME,
                TARGET_COLUMN_NAME,
                NfColumnTypes.NF_UUIDS.column_name,
                NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            ]
        )

    else:
        edges_list = list(
            multi_edged_directed_graph.edges(
                data=NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
                keys=True,
            )
        )

        edges_base_table = DataFrame(
            data=edges_list,
            columns=[
                SOURCE_COLUMN_NAME,
                TARGET_COLUMN_NAME,
                NfColumnTypes.NF_UUIDS.column_name,
                NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            ],
        )

    return edges_base_table
