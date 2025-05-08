from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universes import (
    BIdentityFileSystemObjectUniverses,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.getters.b_identity_file_system_object_universe_getter import (
    get_b_identity_file_system_object_universe,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)
from nf_common.code.services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def run_windows_file_system_utility(
    input_folder: Folders,
    export_hierarchy_register: bool = False,
    export_b_identity_register: bool = True,
    export_to_access: bool = True,
    export_to_sqlite: bool = True,
) -> None:
    output_folder = Folders(
        absolute_path_string=LogFiles.folder_path,
    )

    b_identity_file_system_object_universe = get_b_identity_file_system_object_universe(
        root_file_system_object=input_folder,
    )

    universe_output_root_folder = b_identity_file_system_object_universe.get_universe_output_root_folder(
        universe_output_parent_folder=output_folder,
    )

    if export_hierarchy_register:
        __export_hierarchy_register(
            b_identity_file_system_object_universe=b_identity_file_system_object_universe,
            universe_output_root_folder=universe_output_root_folder,
            export_to_access=export_to_access,
            export_to_sqlite=export_to_sqlite,
        )

    if export_b_identity_register:
        __export_b_identity_register(
            b_identity_file_system_object_universe=b_identity_file_system_object_universe,
            universe_output_root_folder=universe_output_root_folder,
            export_to_access=export_to_access,
            export_to_sqlite=export_to_sqlite,
        )


@run_and_log_function
def __export_hierarchy_register(
    b_identity_file_system_object_universe: BIdentityFileSystemObjectUniverses,
    universe_output_root_folder: Folders,
    export_to_access: bool,
    export_to_sqlite: bool,
) -> None:
    if export_to_access:
        b_identity_file_system_object_universe.b_identity_file_system_object_universe_registers.hierarchy_file_system_object_register.export_register_into_access(
            output_folder=universe_output_root_folder,
        )

    if export_to_sqlite:
        b_identity_file_system_object_universe.b_identity_file_system_object_universe_registers.hierarchy_file_system_object_register.export_register_into_sqlite(
            output_folder=universe_output_root_folder,
        )


@run_and_log_function
def __export_b_identity_register(
    b_identity_file_system_object_universe: BIdentityFileSystemObjectUniverses,
    universe_output_root_folder: Folders,
    export_to_access: bool,
    export_to_sqlite: bool,
) -> None:
    if export_to_access:
        b_identity_file_system_object_universe.b_identity_file_system_object_universe_registers.export_register_into_access(
            output_folder=universe_output_root_folder,
        )

    if export_to_sqlite:
        b_identity_file_system_object_universe.b_identity_file_system_object_universe_registers.export_register_into_sqlite(
            output_folder=universe_output_root_folder,
        )
