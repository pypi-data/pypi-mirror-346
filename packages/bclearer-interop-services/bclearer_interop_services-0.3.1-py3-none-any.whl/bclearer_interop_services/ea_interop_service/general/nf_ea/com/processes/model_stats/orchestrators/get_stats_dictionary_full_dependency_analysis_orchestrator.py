from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    FIRST_CLASS_RELATION_NAME,
    HIGH_ORDER_TYPE_RELATION_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.multi_edged_directed_graph_from_input_edges_table_builder import (
    build_multi_edged_directed_graph_from_input_edges_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.full_dependency_analysis_dictionary_of_stats_common_getter import (
    get_full_dependency_analysis_dictionary_of_stats_common,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.full_dependency_analysis_dictionary_of_stats_getter import (
    get_full_dependency_analysis_dictionary_of_stats,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.full_dependency_analysis_summary_table_getter import (
    get_full_dependency_analysis_summary_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.high_relation_type_dictionary_of_stats_getter import (
    get_high_relation_type_dictionary_of_stats,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.input_edges_table.full_dependencies_input_edges_table_getter import (
    get_full_dependencies_input_edges_table,
)
from networkx import MultiDiGraph
from pandas import DataFrame


def orchestrate_get_stats_dictionary_full_dependency_analysis(
    ea_full_dependencies: DataFrame,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> dict:
    full_dependencies_input_edges_table = get_full_dependencies_input_edges_table(
        ea_full_dependencies=ea_full_dependencies,
        ea_classifiers=ea_classifiers,
        ea_connectors=ea_connectors,
    )

    full_dependency_analysis_model_multi_edged_directed_graph = build_multi_edged_directed_graph_from_input_edges_table(
        input_edges_table=full_dependencies_input_edges_table,
        edge_source_column_name=NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        edge_target_column_name=NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        edge_type_column_name=NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
        ea_classifiers=ea_classifiers,
        is_full_dependencies_edges_table=True,
    )

    full_dependency_analysis_dictionary_of_stats = __get_full_dependency_analysis_dictionary_of_stats(
        full_dependency_analysis_model_multi_edged_directed_graph=full_dependency_analysis_model_multi_edged_directed_graph,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    return full_dependency_analysis_dictionary_of_stats


def __get_full_dependency_analysis_dictionary_of_stats(
    full_dependency_analysis_model_multi_edged_directed_graph: MultiDiGraph,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> dict:
    full_dependency_analysis_dictionary_of_stats_common = get_full_dependency_analysis_dictionary_of_stats_common(
        full_dependency_analysis_model_multi_edged_directed_graph=full_dependency_analysis_model_multi_edged_directed_graph,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    full_dependency_analysis_dictionary_of_stats_high_order_types = get_high_relation_type_dictionary_of_stats(
        full_dependency_analysis_dictionary_of_stats_common=full_dependency_analysis_dictionary_of_stats_common,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        high_relation_type_name=HIGH_ORDER_TYPE_RELATION_NAME,
    )

    full_dependency_analysis_dictionary_of_stats_first_class_relations = get_high_relation_type_dictionary_of_stats(
        full_dependency_analysis_dictionary_of_stats_common=full_dependency_analysis_dictionary_of_stats_common,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        high_relation_type_name=FIRST_CLASS_RELATION_NAME,
    )

    full_dependency_analysis_summary_table = get_full_dependency_analysis_summary_table(
        full_dependency_analysis_dictionary_of_stats_high_order_types=full_dependency_analysis_dictionary_of_stats_high_order_types,
        full_dependency_analysis_dictionary_of_stats_common=full_dependency_analysis_dictionary_of_stats_common,
        full_dependency_analysis_dictionary_of_stats_first_class_relations=full_dependency_analysis_dictionary_of_stats_first_class_relations,
    )

    full_dependency_analysis_dictionary_of_stats = get_full_dependency_analysis_dictionary_of_stats(
        full_dependency_analysis_dictionary_of_stats_high_order_types=full_dependency_analysis_dictionary_of_stats_high_order_types,
        full_dependency_analysis_dictionary_of_stats_first_class_relations=full_dependency_analysis_dictionary_of_stats_first_class_relations,
        full_dependency_analysis_summary_table=full_dependency_analysis_summary_table,
        full_dependency_analysis_dictionary_of_stats_common=full_dependency_analysis_dictionary_of_stats_common,
    )

    return full_dependency_analysis_dictionary_of_stats
