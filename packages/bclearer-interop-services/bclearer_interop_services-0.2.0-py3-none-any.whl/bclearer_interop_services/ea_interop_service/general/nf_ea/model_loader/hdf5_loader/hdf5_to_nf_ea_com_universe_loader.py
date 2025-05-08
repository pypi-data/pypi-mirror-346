from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def load_hdf5_to_nf_ea_com_universe(
    ea_tools_session_manager: EaToolsSessionManagers,
    hdf5_file: Files,
    short_name: str,
) -> NfEaComUniverses:
    new_nf_ea_com_universe = __get_empty_nf_ea_com_universe(
        ea_tools_session_manager=ea_tools_session_manager,
        short_name=short_name,
    )

    new_nf_ea_com_universe.nf_ea_com_registry.import_registry_from_hdf5(
        hdf5_file=hdf5_file
    )

    return new_nf_ea_com_universe


def __get_empty_nf_ea_com_universe(
    ea_tools_session_manager: EaToolsSessionManagers,
    short_name: str,
) -> NfEaComUniverses:
    ea_repository = ea_tools_session_manager.create_empty_ea_repository_with_short_name(
        short_name=short_name
    )

    nf_ea_com_universe_manager = (
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
    )

    nf_ea_com_universe = nf_ea_com_universe_manager.nf_ea_com_universe_dictionary[
        ea_repository
    ]

    return nf_ea_com_universe
