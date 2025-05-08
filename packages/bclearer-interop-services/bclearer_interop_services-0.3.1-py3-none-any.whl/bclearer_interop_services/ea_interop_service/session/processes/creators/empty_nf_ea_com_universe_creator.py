from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def create_empty_nf_ea_universe(
    ea_tools_session_manager: EaToolsSessionManagers,
    short_name: str,
):
    empty_universe_repository = ea_tools_session_manager.create_empty_ea_repository_with_short_name(
        short_name=short_name
    )

    nf_ea_com_universe_manager = (
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
    )

    empty_nf_ea_com_universe = nf_ea_com_universe_manager.nf_ea_com_universe_dictionary[
        empty_universe_repository
    ]

    return empty_nf_ea_com_universe
