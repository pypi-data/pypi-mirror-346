from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.nf_ea_com_initialiser import (
    initialise_nf_ea_com_dictionary,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.temporary.nf_ea_com_dictionary_to_nf_ea_com_universe_convertor import (
    convert_nf_ea_com_dictionary_to_nf_ea_com_universe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.table_lists.connector_tables_converter import (
    convert_connector_tables,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.table_lists.element_tables_converter import (
    convert_element_tables,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.table_lists.stereotype_group_tables_converter import (
    convert_stereotype_group_tables,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.table_lists.stereotype_tables_converter import (
    convert_stereotype_tables,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.table_lists.stereotype_usage_tables_converter import (
    convert_stereotype_usage_tables,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def convert_standard_tables_dictionary_to_nf_ea_com_universe(
    ea_tools_session_manager: EaToolsSessionManagers,
    standard_tables_dictionary: dict,
    package_base_names: list,
    object_base_names: list,
    connector_base_names: list,
    stereotype_group_base_names: list,
    stereotype_base_names: list,
    stereotype_usage_base_names: list,
    short_name: str,
) -> NfEaComUniverses:
    nf_ea_com_dictionary = (
        initialise_nf_ea_com_dictionary()
    )

    nf_ea_com_dictionary = convert_element_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        element_base_names=package_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        collection_type=NfEaComCollectionTypes.EA_PACKAGES,
    )

    nf_ea_com_dictionary = convert_element_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        element_base_names=object_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
    )

    nf_ea_com_dictionary = convert_connector_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        connector_base_names=connector_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
    )

    nf_ea_com_dictionary = convert_stereotype_group_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        stereotype_group_base_names=stereotype_group_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
    )

    nf_ea_com_dictionary = convert_stereotype_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        stereotype_base_names=stereotype_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
    )

    nf_ea_com_dictionary = convert_stereotype_usage_tables(
        standard_tables_dictionary=standard_tables_dictionary,
        stereotype_usage_base_names=stereotype_usage_base_names,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
    )

    nf_ea_com_universe = convert_nf_ea_com_dictionary_to_nf_ea_com_universe(
        ea_tools_session_manager=ea_tools_session_manager,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        short_name=short_name,
    )

    return nf_ea_com_universe
