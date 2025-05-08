from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def get_b_identity_folder_id_b_identity_component_id_sum(
    b_identity_file_system_object_registry,
    hierarchy_folder: HierarchyFolders,
) -> int:
    from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universe_registers import (
        BIdentityFileSystemObjectUniverseRegisters,
    )

    if not isinstance(
        b_identity_file_system_object_registry,
        BIdentityFileSystemObjectUniverseRegisters,
    ):
        raise TypeError

    b_identity_folder_id_b_identity_component_id_sum = (
        0
    )

    # TODO: Temporary bIdentity given, based on the addition of the id identities of the folder's children (one level)
    #  - to be discussed
    for (
        hierarchy_folder_child_object
    ) in (
        hierarchy_folder.child_hierarchy_file_system_objects
    ):
        b_identity_child_object = b_identity_file_system_object_registry.get_identity_b_identity_file_system_object_from_hierarchy_object(
            hierarchy_file_system_object=hierarchy_folder_child_object,
        )

        b_identity_folder_id_b_identity_component_id_sum += (
            b_identity_child_object.id_b_identity
        )

    return b_identity_folder_id_b_identity_component_id_sum
