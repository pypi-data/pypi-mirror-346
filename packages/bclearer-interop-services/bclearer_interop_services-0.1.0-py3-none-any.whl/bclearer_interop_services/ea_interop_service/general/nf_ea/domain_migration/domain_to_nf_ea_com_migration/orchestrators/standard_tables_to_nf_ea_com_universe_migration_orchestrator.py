from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.standard_tables_dictionary_to_nf_ea_com_universe_converter import (
    convert_standard_tables_dictionary_to_nf_ea_com_universe,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def orchestrate_standard_tables_to_nf_ea_com_universe_migration(
    ea_tools_session_manager: EaToolsSessionManagers,
    standard_tables_dictionary: dict,
    object_csv_base_names: list,
    package_csv_base_names: list,
    connector_csv_base_names: list,
    stereotype_group_sheet_names: list,
    stereotype_sheet_names: list,
    stereotype_usage_sheet_names: list,
    short_name: str,
) -> NfEaComUniverses:
    nf_ea_com_universe = convert_standard_tables_dictionary_to_nf_ea_com_universe(
        ea_tools_session_manager=ea_tools_session_manager,
        standard_tables_dictionary=standard_tables_dictionary,
        package_base_names=package_csv_base_names,
        object_base_names=object_csv_base_names,
        connector_base_names=connector_csv_base_names,
        stereotype_group_base_names=stereotype_group_sheet_names,
        stereotype_base_names=stereotype_sheet_names,
        stereotype_usage_base_names=stereotype_usage_sheet_names,
        short_name=short_name,
    )

    return nf_ea_com_universe
