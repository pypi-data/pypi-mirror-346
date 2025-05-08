import os

from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.native_xml_loader.nf_ea_xml_load_to_empty_ea_model_orchestrator import (
    orchestrate_nf_ea_xml_load_to_empty_ea_model,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def orchestrate_nf_ea_com_universe_to_eapx_migration(
    ea_tools_session_manager: EaToolsSessionManagers,
    nf_ea_com_universe: NfEaComUniverses,
    short_name: str,
    output_folder: Folders,
):
    ea_export_folder_path = os.path.join(
        output_folder.absolute_path_string,
        short_name,
        short_name + "_ea_export",
    )

    ea_repository_file_path = (
        os.path.join(
            ea_export_folder_path,
            short_name
            + "_ea_export.eapx",
        )
    )

    ea_repository_file = Files(
        absolute_path_string=ea_repository_file_path
    )

    output_xml_file_full_path = (
        os.path.join(
            ea_export_folder_path,
            short_name
            + "_ea_export.xml",
        )
    )

    orchestrate_nf_ea_xml_load_to_empty_ea_model(
        ea_tools_session_manager=ea_tools_session_manager,
        nf_ea_com_universe=nf_ea_com_universe,
        output_xml_file_full_path=output_xml_file_full_path,
        ea_repository_file=ea_repository_file,
        short_name=short_name
        + "_ea_export",
    )
