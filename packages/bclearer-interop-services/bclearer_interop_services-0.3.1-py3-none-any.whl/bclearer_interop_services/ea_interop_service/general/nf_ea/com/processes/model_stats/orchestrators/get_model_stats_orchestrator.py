from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.dictionary_services.dictionary_concatenator import (
    concatenate_dictionaries,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.orchestrators.get_stats_dictionary_base_model_orchestrator import (
    orchestrate_get_stats_dictionary_base_model,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.orchestrators.get_stats_dictionary_base_model_proxy_connectors_processed_orchestrator import (
    orchestrate_get_stats_dictionary_base_model_proxy_connectors_processed,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.orchestrators.get_stats_dictionary_full_dependency_analysis_orchestrator import (
    orchestrate_get_stats_dictionary_full_dependency_analysis,
)


def orchestrate_get_model_stats(
    nf_ea_com_registry,
) -> dict:
    ea_classifiers = (
        nf_ea_com_registry.get_ea_classifiers()
    )

    ea_packages = (
        nf_ea_com_registry.get_ea_packages()
    )

    ea_connectors = (
        nf_ea_com_registry.get_ea_connectors()
    )

    ea_stereotypes = (
        nf_ea_com_registry.get_ea_stereotypes()
    )

    ea_stereotype_usage = nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.STEREOTYPE_USAGE
    ]

    ea_full_dependencies = (
        nf_ea_com_registry.get_ea_full_dependencies()
    )

    stats_dictionary_base_model = orchestrate_get_stats_dictionary_base_model(
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    stats_dictionary_base_model_proxy_connectors_processed = orchestrate_get_stats_dictionary_base_model_proxy_connectors_processed(
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    stats_dictionary_full_dependency_analysis = orchestrate_get_stats_dictionary_full_dependency_analysis(
        ea_full_dependencies=ea_full_dependencies,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    model_full_stats_dictionary = concatenate_dictionaries(
        dictionaries=[
            stats_dictionary_base_model,
            stats_dictionary_base_model_proxy_connectors_processed,
            stats_dictionary_full_dependency_analysis,
        ]
    )

    return model_full_stats_dictionary
