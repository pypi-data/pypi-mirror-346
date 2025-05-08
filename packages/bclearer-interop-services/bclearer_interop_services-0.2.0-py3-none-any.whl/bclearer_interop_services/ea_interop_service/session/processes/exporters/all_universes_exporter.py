from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def export_all_universes(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder: Folders,
):
    __create_and_export_nf_ea_com(
        ea_tools_session_manager=ea_tools_session_manager,
        output_folder_name=output_folder.absolute_path_string,
    )

    __export_nf_ea_sql(
        ea_tools_session_manager=ea_tools_session_manager,
        output_folder_name=output_folder.absolute_path_string,
    )

    __export_ea_sql(
        ea_tools_session_manager=ea_tools_session_manager,
        output_folder_name=output_folder.absolute_path_string,
    )


def __create_and_export_nf_ea_com(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
):
    nf_ea_com_universe_manager = (
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
    )

    nf_ea_com_universe_manager.export_all_registries(
        output_folder_name=output_folder_name
    )


def __export_nf_ea_sql(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
):
    nf_ea_sql_universe_manager = (
        ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager
    )

    nf_ea_sql_universe_manager.export_all_registries(
        output_folder_name=output_folder_name
    )


def __export_ea_sql(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
):
    ea_sql_universe_manager = (
        ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager
    )
    ea_sql_universe_manager.export_all_registries(
        output_folder_name=output_folder_name
    )
