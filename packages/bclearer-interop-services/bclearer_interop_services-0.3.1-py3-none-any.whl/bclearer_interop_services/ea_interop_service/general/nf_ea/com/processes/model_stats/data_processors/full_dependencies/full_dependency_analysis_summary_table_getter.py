from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.common_data_visualisation.dictionary_of_stats_summary_table_common_getter import (
    get_dictionary_of_stats_summary_table_common,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    FIRST_CLASS_RELATION_NAME,
    FULL_DEPENDENCIES_NAME,
    FULL_DEPENDENCIES_SUMMARY_TABLE_NAME,
    HIGH_ORDER_TYPE_RELATION_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.dictionary_of_stats_summary_table_high_relation_type_getter import (
    get_dictionary_of_stats_summary_table_high_relation_type,
)
from pandas import DataFrame, concat


def get_full_dependency_analysis_summary_table(
    full_dependency_analysis_dictionary_of_stats_high_order_types: dict,
    full_dependency_analysis_dictionary_of_stats_common: dict,
    full_dependency_analysis_dictionary_of_stats_first_class_relations: dict,
) -> DataFrame:

    full_dependencies_path_analysis_master_table = full_dependency_analysis_dictionary_of_stats_common[
        FULL_DEPENDENCIES_SUMMARY_TABLE_NAME
    ]

    full_dependency_analysis_summary_table_common = get_dictionary_of_stats_summary_table_common(
        dictionary_of_stats_common=full_dependency_analysis_dictionary_of_stats_common,
        output_summary_table_prefix=FULL_DEPENDENCIES_NAME,
    )

    full_dependency_analysis_summary_table_high_order_types = get_dictionary_of_stats_summary_table_high_relation_type(
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
        high_relation_type_dictionary_of_stats=full_dependency_analysis_dictionary_of_stats_high_order_types,
        high_relation_type_name=HIGH_ORDER_TYPE_RELATION_NAME,
    )

    full_dependency_analysis_summary_table_first_class_relations = get_dictionary_of_stats_summary_table_high_relation_type(
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
        high_relation_type_dictionary_of_stats=full_dependency_analysis_dictionary_of_stats_first_class_relations,
        high_relation_type_name=FIRST_CLASS_RELATION_NAME,
    )

    full_dependency_analysis_summary_table = concat(
        [
            full_dependency_analysis_summary_table_common,
            full_dependency_analysis_summary_table_high_order_types,
            full_dependency_analysis_summary_table_first_class_relations,
        ]
    ).reindex()

    return full_dependency_analysis_summary_table
