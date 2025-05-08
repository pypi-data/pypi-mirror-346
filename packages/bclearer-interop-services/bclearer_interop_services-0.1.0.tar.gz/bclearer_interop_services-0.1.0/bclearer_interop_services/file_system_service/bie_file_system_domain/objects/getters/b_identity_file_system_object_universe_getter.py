from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universes import (
    BIdentityFileSystemObjectUniverses,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def get_b_identity_file_system_object_universe(
    root_file_system_object: Folders,
) -> BIdentityFileSystemObjectUniverses:
    b_identity_file_system_object_universe = BIdentityFileSystemObjectUniverses(
        root_file_system_object=root_file_system_object,
    )

    # TODO: export the universe to a database: b_identity_file_system_object_universe
    #  For the moment, it only exports the file system object register
    # universe_in_b_datasets_format = \
    #     b_identity_file_system_object_universe.export_universe_in_b_datasets_format(
    #         output_folder=output_folder)

    return b_identity_file_system_object_universe
