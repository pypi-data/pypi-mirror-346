from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)


def add_model_stats_tables_to_nf_ea_com_registry(
    nf_ea_com_registry,
    model_stats_tables: dict,
):
    for (
        collection
    ) in NfEaComCollectionTypes:
        for (
            stats_table_name,
            stats_table,
        ) in model_stats_tables.items():
            if (
                collection.collection_name
                == stats_table_name
            ):
                nf_ea_com_registry.dictionary_of_collections[
                    collection
                ] = stats_table
