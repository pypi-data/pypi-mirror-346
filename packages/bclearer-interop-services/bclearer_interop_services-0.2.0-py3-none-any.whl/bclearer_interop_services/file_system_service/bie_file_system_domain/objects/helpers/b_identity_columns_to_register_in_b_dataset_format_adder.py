from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_files import (
    BIdentityFiles,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_folders import (
    BIdentityFolders,
)


def add_b_identity_columns_to_register_in_b_dataset_format(
    b_identity_file_system_object_universe_register,
    register_in_b_datasets_format: dict,
    hierarchy_file_system_object_row_dictionary: dict,
    hierarchy_file_system_object_uuid: str,
) -> None:
    from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universe_registers import (
        BIdentityFileSystemObjectUniverseRegisters,
    )

    if not isinstance(
        b_identity_file_system_object_universe_register,
        BIdentityFileSystemObjectUniverseRegisters,
    ):
        raise TypeError

    hierarchy_file_system_object = b_identity_file_system_object_universe_register.get_hierarchy_file_system_object_by_uuid(
        hierarchy_file_system_object_uuid=hierarchy_file_system_object_uuid,
    )

    if not hierarchy_file_system_object:
        raise NotImplementedError

    b_identity_file_system_object = b_identity_file_system_object_universe_register.get_identity_b_identity_file_system_object_from_hierarchy_object(
        hierarchy_file_system_object=hierarchy_file_system_object,
    )

    parent_b_identity_file_system_object = b_identity_file_system_object_universe_register.get_identity_b_identity_file_system_object_from_hierarchy_object(
        hierarchy_file_system_object=hierarchy_file_system_object.parent_hierarchy_folder,
    )

    if (
        not parent_b_identity_file_system_object
    ):
        parent_id_b_identity_file_system_object = (
            ""
        )

    else:
        parent_id_b_identity_file_system_object = (
            parent_b_identity_file_system_object.id_b_identity
        )

    universe_in_b_datasets_format_row_dictionary = {
        "id_b_identities": b_identity_file_system_object.id_b_identity,
        "b_identity_file_system_object_types": type(
            b_identity_file_system_object,
        ).__name__,
        "parent_id_b_identity": parent_id_b_identity_file_system_object,
    }

    if isinstance(
        b_identity_file_system_object,
        BIdentityFolders,
    ):
        universe_in_b_datasets_format_row_dictionary.update(
            {
                "id_b_identity_component_id_sum": b_identity_file_system_object.id_b_identity_component_id_sum,
                "b_identity_component_immutable_stage_sum": b_identity_file_system_object.b_identity_component_immutable_stage_sum,
            },
        )

    elif isinstance(
        b_identity_file_system_object,
        BIdentityFiles,
    ):
        universe_in_b_datasets_format_row_dictionary.update(
            {
                "b_identity_immutable_stage": b_identity_file_system_object.b_identity_immutable_stage,
            },
        )

    else:
        raise TypeError

    universe_in_b_datasets_format_row_dictionary.update(
        hierarchy_file_system_object_row_dictionary,
    )

    register_in_b_datasets_format[
        b_identity_file_system_object.id_b_identity
    ] = universe_in_b_datasets_format_row_dictionary
