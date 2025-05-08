from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.common_data_visualisation.dictionary_of_stats_summary_table_common_getter import (
    get_dictionary_of_stats_summary_table_common,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    GENERAL_NAME,
    GENERAL_SUMMARY_TABLE_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.multi_edged_directed_graph_from_input_edges_table_builder import (
    build_multi_edged_directed_graph_from_input_edges_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.input_edges_table.common_input_edges_table_getter import (
    get_common_input_edges_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.visualisation.base_model_dictionary_of_stats_getter import (
    get_base_model_dictionary_of_stats,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.visualisation.summary_table_to_dictionary_of_stats_adder import (
    add_summary_table_to_dictionary_of_stats,
)
from networkx import MultiDiGraph
from pandas import DataFrame


def orchestrate_get_stats_dictionary_base_model(
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> dict:
    base_model_input_edges_table = get_common_input_edges_table(
        ea_classifiers=ea_classifiers,
        ea_connectors=ea_connectors,
    )

    base_model_multi_edged_directed_graph = build_multi_edged_directed_graph_from_input_edges_table(
        input_edges_table=base_model_input_edges_table,
        edge_source_column_name=NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        edge_target_column_name=NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        edge_type_column_name=NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
        ea_classifiers=ea_classifiers,
        is_full_dependencies_edges_table=False,
    )

    base_model_dictionary_of_stats = __get_base_model_dictionary_of_stats(
        base_model_multi_edged_directed_graph=base_model_multi_edged_directed_graph,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        output_summary_table_prefix=GENERAL_NAME,
    )

    return (
        base_model_dictionary_of_stats
    )


def __get_base_model_dictionary_of_stats(
    base_model_multi_edged_directed_graph: MultiDiGraph,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
    output_summary_table_prefix: str,
) -> dict:
    base_model_dictionary_of_stats = get_base_model_dictionary_of_stats(
        base_model_multi_edged_directed_graph=base_model_multi_edged_directed_graph,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    base_model_dictionary_of_stats_summary_table = get_dictionary_of_stats_summary_table_common(
        dictionary_of_stats_common=base_model_dictionary_of_stats,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    base_model_dictionary_of_stats = add_summary_table_to_dictionary_of_stats(
        stats_summary_table=base_model_dictionary_of_stats_summary_table,
        dictionary_of_stats=base_model_dictionary_of_stats,
        stats_summary_table_name=GENERAL_SUMMARY_TABLE_NAME,
    )

    return (
        base_model_dictionary_of_stats
    )
