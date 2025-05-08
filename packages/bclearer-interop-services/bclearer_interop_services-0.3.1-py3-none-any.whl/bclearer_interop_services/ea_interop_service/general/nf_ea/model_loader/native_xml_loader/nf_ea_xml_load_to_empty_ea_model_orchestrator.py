from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.native_xml_loader.dictionary_of_dataframes_getter import (
    get_dictionary_of_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.native_xml_loader.xml_file_creator_and_loader import (
    create_and_load_xml_file,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_empty_repository_getter import (
    get_ea_repository_for_empty_ea_model,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def orchestrate_nf_ea_xml_load_to_empty_ea_model(
    ea_tools_session_manager: EaToolsSessionManagers,
    nf_ea_com_universe: NfEaComUniverses,
    output_xml_file_full_path: str,
    ea_repository_file: Files,
    short_name: str,
):
    ea_repository = get_ea_repository_for_empty_ea_model(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    nf_ea_com_dataframes_dictionary = get_dictionary_of_dataframes(
        nf_ea_com_universe=nf_ea_com_universe
    )

    create_and_load_xml_file(
        ea_tools_session_manager=ea_tools_session_manager,
        output_xml_file_full_path=output_xml_file_full_path,
        ea_repository=ea_repository,
        nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary,
    )
