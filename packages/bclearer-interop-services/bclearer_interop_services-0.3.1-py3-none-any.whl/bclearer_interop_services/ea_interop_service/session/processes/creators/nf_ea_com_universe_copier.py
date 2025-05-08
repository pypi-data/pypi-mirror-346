def register_universe_copy(
    ea_tools_session_manager,
    nf_ea_com_universe,
    ea_repository_copy,
):
    nf_ea_com_universe_manager = (
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
    )

    nf_ea_com_universe_manager.nf_ea_com_universe_dictionary[
        ea_repository_copy
    ] = nf_ea_com_universe
