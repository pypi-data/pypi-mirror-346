from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.creators.new_nf_ea_com_universe_using_file_creator import (
    create_new_nf_ea_com_universe_using_file,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def load_ea_model_into_hdf5(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository_file: Files,
    short_name: str,
    hdf5_file: Files,
):
    loaded_universe = create_new_nf_ea_com_universe_using_file(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    loaded_universe.nf_ea_com_registry.export_registry_to_hdf5(
        hdf5_file=hdf5_file
    )
