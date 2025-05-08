from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.native_xml_loader.xml_file_creator_and_loader import (
    create_and_load_xml_file,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def orchestrate_nf_ea_xml_load(
    nf_ea_com_dataframes_dictionary: dict,
    output_xml_file_full_path: str,
    default_model_package_ea_guid: str = None,
    just_create_xml=False,
):
    with EaToolsSessionManagers() as ea_tools_session_manager:
        log_message(
            message="Starting xml load to "
            + output_xml_file_full_path
        )

        ea_repository = (
            ea_tools_session_manager.create_ea_repository()
        )

        create_and_load_xml_file(
            ea_tools_session_manager=ea_tools_session_manager,
            output_xml_file_full_path=output_xml_file_full_path,
            ea_repository=ea_repository,
            nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary,
            default_model_package_ea_guid=default_model_package_ea_guid,
            just_create_xml=just_create_xml,
        )
