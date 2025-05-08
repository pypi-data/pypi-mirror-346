from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.orchestrators.nf_ea_com_universe_to_eapx_migration_orchestator import (
    orchestrate_nf_ea_com_universe_to_eapx_migration,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.orchestrators.standard_tables_to_nf_ea_com_universe_migration_orchestrator import (
    orchestrate_standard_tables_to_nf_ea_com_universe_migration,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.exporters.all_universes_exporter import (
    export_all_universes,
)
from bclearer_interop_services.excel.xlsx_to_dataframe_dictionary_converter import (
    covert_xlxs_to_dataframe_dictionary,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def orchestrate_xlsx_to_eapx_migration(
    input_file: Files,
    output_folder: Folders,
    short_name: str,
    package_sheet_names: list,
    classifier_sheet_names: list,
    connector_sheet_names: list,
    stereotype_group_sheet_names: list,
    stereotype_sheet_names: list,
    stereotype_usage_sheet_names: list,
):
    log_message(
        "========== Started Converting xlsx to eapx =========="
    )

    log_message(
        "Input xlsx file - "
        + input_file.absolute_path_string
    )

    log_message(
        "Output folder - "
        + output_folder.absolute_path_string
    )

    standard_tables_dictionary = covert_xlxs_to_dataframe_dictionary(
        xlsx_file=input_file
    )

    with EaToolsSessionManagers() as ea_tools_session_manager:
        nf_ea_com_universe = orchestrate_standard_tables_to_nf_ea_com_universe_migration(
            ea_tools_session_manager=ea_tools_session_manager,
            standard_tables_dictionary=standard_tables_dictionary,
            package_csv_base_names=package_sheet_names,
            object_csv_base_names=classifier_sheet_names,
            connector_csv_base_names=connector_sheet_names,
            stereotype_group_sheet_names=stereotype_group_sheet_names,
            stereotype_sheet_names=stereotype_sheet_names,
            stereotype_usage_sheet_names=stereotype_usage_sheet_names,
            short_name=short_name,
        )

        orchestrate_nf_ea_com_universe_to_eapx_migration(
            ea_tools_session_manager=ea_tools_session_manager,
            nf_ea_com_universe=nf_ea_com_universe,
            short_name=short_name,
            output_folder=output_folder,
        )

        export_all_universes(
            ea_tools_session_manager=ea_tools_session_manager,
            output_folder=output_folder,
        )

    log_message(
        "========== Finished Converting xlsx to eapx =========="
    )
